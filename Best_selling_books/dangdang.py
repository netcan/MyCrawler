import requests, re, os
import pandas as pd
from util.downloader import Downloader
from util.redisCache import RedisCache
from collections import OrderedDict, namedtuple
from lxml.html import fromstring


class Dangdang:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/64.0.3282.186 Safari/537.36 '
    }
    url = 'http://bang.dangdang.com/books/bestsellers/{}-{}-{}'

    def __init__(self):
        self.books_list_info = namedtuple('bli', ['category', 'list'])
        self.bs_books_list = []
        self.category_dict = {}
        self.downloader = Downloader(0, RedisCache())
        pass

    def get_category_list(self):
        url = 'http://bang.dangdang.com/books/bestsellers/'
        res = requests.get(url, headers=self.headers)
        html = fromstring(res.text)
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
                    url=book_url
                )
                # book.update(self.get_book_info(book_url))
                # print(book)
                books.append(book)

        self.bs_books_list.append(
            self.books_list_info(self.category_dict[cid], books)
        )

    def get_book_info(self, book_url):
        res = requests.get(book_url, headers=self.headers)
        html = fromstring(res.text)
        return {
            'ISBN': re.findall('国际标准书号ISBN：(\d+)', html.cssselect('ul.key')[0].text_content())[0]
        }

    def save_books_list(self):
        if not os.path.exists('results'):
            os.mkdir('results')

        writer = pd.ExcelWriter('results/当当网畅销书汇总 by netcan.xlsx')
        for books in self.bs_books_list:
            books_df = pd.DataFrame(books.list)
            books_df.to_excel(writer, books.category.replace('/', ','), index=False)
        writer.save()

    def get_all(self):
        self.get_category_list()
        for category, cname in self.category_dict.items():
            print(cname)
            self.get_books_list(category)


if __name__ == '__main__':
    dangdang = Dangdang()
    dangdang.get_all()
