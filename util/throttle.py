from urllib.parse import urlparse
import time


class Throttle:
    def __init__(self, delay):
        self.delay = delay
        self.domains = {}

    def wait(self, url):
        domain = urlparse(url).netloc
        last_accessed = self.domains.get(domain)
        if self.delay > 0 and last_accessed is not None:
            remain = self.delay - (time.time() - last_accessed)
            if remain > 0:
                time.sleep(remain)
        self.domains[domain] = time.time()
