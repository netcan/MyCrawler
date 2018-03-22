import re, os
import pandas as pd
import pickle, threading, time
from util.downloader import Downloader
from util.redisCache import RedisCache
from collections import OrderedDict
from lxml.html import fromstring


class Dangdang:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/64.0.3282.186 Safari/537.36 '
    }
    url = 'http://bang.dangdang.com/books/bestsellers/{}-{}-{}'

    def __init__(self):
        if not os.path.exists('output'):
            os.mkdir('output')
        self.bs_books = {}
        self.stopped = False
        self.queue = []
        self.category_dict = {}
        self.downloader = Downloader(0, RedisCache())
        pass

    def get_category_list(self):
        url = 'http://bang.dangdang.com/books/bestsellers/'
        res = self.downloader(url)
        html = fromstring(res)
        self.category_dict = {
            cid.attrib['category_path']: cid.cssselect('a')[0].text for cid in
            html.cssselect('#sortRanking .side_nav')
        }

    def get_books_list(self, cid='01.03.00.00.00.00', idx='month-2018-2-2', page=1):
        books = []
        for page in range(page, 25 + 1):
            print('page =', page)
            res = self.downloader(self.url.format(cid, idx, page))
            html = fromstring(res)
            for lst in html.cssselect('.bang_list li'):
                book_url = lst.cssselect('.name a')[0].attrib['href']
                try:
                    publish_date = re.findall('\d{4}-\d{2}-\d{2}', lst.cssselect('.publisher_info')[0].text_content())[0]
                except IndexError:
                    publish_date = None
                book = OrderedDict(
                    rank=lst.cssselect('.number')[0].text,
                    name=lst.cssselect('.name a')[0].attrib['title'],
                    publish_date=publish_date,
                    ISBN=None,
                    price=None,
                    url=book_url
                )
                # book.update(self.get_book_info(book_url))
                # print(book)
                books.append(book)

        self.bs_books[cid] = books

    def _update_book_info(self, cid, bid, book_url):
        book = self.bs_books[cid][bid]
        if not book['ISBN'] or not book['price']:
            res = self.downloader(book_url)
            html = fromstring(res)
            try:
                book.update({
                    'ISBN': re.findall('国际标准书号ISBN：(\d+)', html.cssselect('ul.key')[0].text_content())[0],
                    'price': html.cssselect('#original-price')[0].text_content().strip()
                })
            except IndexError:
                print(book_url)

            print(book['name'], book['ISBN'])

    def update_books_info(self, max_threads=4):
        self.queue = []
        for cid, books_info in self.bs_books.items():
            for bid, book_info in enumerate(books_info):
                self.queue.append((cid, bid, book_info['url']))

        def mt():
            while not self.stopped and len(self.queue):
                book_ifo = self.queue.pop()
                self._update_book_info(*book_ifo)
                print('remain: ', len(self.queue))

        threads = []
        while not self.stopped and (threads or len(self.queue)):
            for thread in threads:
                if not thread.is_alive():
                    threads.remove(thread)

            while len(threads) < max_threads and len(self.queue):
                thread = threading.Thread(target=mt, daemon=True)
                thread.start()
                threads.append(thread)

            # don't block it
            # for thread in threads:
            #     thread.join()

            time.sleep(1)

        self.save_obj()

    def save_obj(self):
        with open('output/category_dict.pkl', 'wb') as f:
            pickle.dump(self.category_dict, f, pickle.HIGHEST_PROTOCOL)
        with open('output/bs_books.pkl', 'wb') as f:
            pickle.dump(self.bs_books, f, pickle.HIGHEST_PROTOCOL)

    def load_obj(self):
        with open('output/category_dict.pkl', 'rb') as f:
            self.category_dict = pickle.load(f)
        with open('output/bs_books.pkl', 'rb') as f:
            self.bs_books = pickle.load(f)

    def save_books_list(self):
        writer = pd.ExcelWriter('output/当当网畅销书汇总 by netcan.xlsx')
        for cid, books in self.bs_books.items():
            books_df = pd.DataFrame(books)
            books_df.to_excel(writer, self.category_dict[cid].replace('/', ''), index=False)
        writer.save()

    def get_all(self):
        self.get_category_list()
        for cnt, (cid, cname) in enumerate(self.category_dict.items()):
            print(cname, cnt + 1, '/', len(self.category_dict))
            self.get_books_list(cid)
        self.save_obj()


if __name__ == '__main__':
    dangdang = Dangdang()
    dangdang.get_all()
