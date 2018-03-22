import redis
from redis import StrictRedis


class RedisQueue:
    def __init__(self, client=None, name='crawler'):
        assert isinstance(client, (redis.client.StrictRedis, type(None)))
        self.client = StrictRedis(host='localhost', port=6379, db=0) \
            if client is None else client
        self.queue = 'queue:%s' % name
        self.seen_set = 'set:%s' % name
        self.depth = 'depth:%s' % name

    def __len__(self):
        return self.client.llen(self.queue)

    def __repr__(self):
        return str(self.client.lrange(self.queue, 0, -1))

    def already_seen(self, element):
        return self.client.sismember(self.seen_set, element)

    def push(self, element):
        if isinstance(element, list):
            element = list(filter(lambda e: not self.already_seen(e), element))
            if element:
                self.client.lpush(self.queue, *element)
                self.client.sadd(self.seen_set, *element)
        elif not self.already_seen(element):
            self.client.lpush(self.queue, element)
            self.client.sadd(self.seen_set, element)

    def pop(self):
        return self.client.rpop(self.queue).decode('utf-8')

    def clear(self):
        self.client.delete(self.queue, self.seen_set, self.depth)

    def set_depth(self, element, depth):
        return self.client.hset(self.depth, element, depth)

    def get_depth(self, element):
        return int(self.client.hget(self.depth, element) or 0)
