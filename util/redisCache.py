from redis import StrictRedis
import json, zlib


class RedisCache:
    def __init__(self, client=None, compress=True, encoding='utf8'):
        self.client = StrictRedis(host='localhost', port=6379, db=0) \
            if not client else client
        self.encoding = encoding
        self.compress = compress

    def __getitem__(self, url):
        record = self.client.get(url)
        if record and self.compress:
            record = zlib.decompress(self.client.get(url))

        if record is None:
            raise KeyError(url + 'dose not exist')
        else:
            return json.loads(record.decode(self.encoding))

    def __setitem__(self, url, result):
        self.client.set(url, zlib.compress(json.dumps(result).encode(self.encoding)))

