from util.throttle import Throttle
import requests


class Downloader:
    def __init__(self, delay=3, cache={}):
        self.throttle = Throttle(delay)
        self.user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/61.0.3163.100 Safari/537.36"
        self.proxies = dict(http='socks5://127.0.0.1:1086',
                            https='socks5://127.0.0.1:1086')
        self.cache = cache
        self.num_retries = None

    def __call__(self, url, num_retries=2):
        self.num_retries = num_retries
        try:
            result = self.cache[url]
            print('Load from cache: ' + url)
        except KeyError:
            result = None
        if result and num_retries and 500 <= result['code'] < 600:
            result = None

        if result is None:
            self.throttle.wait(url)
            result = self.download(url)
            self.cache[url] = result

        return result['html']

    def download(self, url):
        print('Downloading: ' + url)
        try:
            resp = requests.get(url, headers={
                'User-Agent': self.user_agent
            }, proxies=self.proxies)
            resp.encoding = 'utf8'
            html = resp.text
            if resp.status_code >= 400:
                print('Download error: ' + html)
                # 重下
                if 500 <= resp.status_code < 600 and self.num_retries:
                    self.num_retries -= self.num_retries
                    return self.download(url)
        except requests.exceptions.RequestException as e:
            html = None
            print('Download error: ' + e)

        return {'html': html, 'code': resp.status_code}
