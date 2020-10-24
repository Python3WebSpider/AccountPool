import random
import redis
from accountpool.setting import *


class RedisClient(object):
    """
    redis client
    """
    
    def __init__(self, type, website, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        init redis client
        :param host: redis host
        :param port: redis port
        :param password: redis password
        """
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)
        self.type = type
        self.website = website
    
    def name(self):
        """
        get hash name
        :return: name of hash
        """
        return f'{self.type}:{self.website}'
    
    def set(self, username, value):
        """
        set key-value
        :param username: username
        :param value: password or cookies
        :return:
        """
        return self.db.hset(self.name(), username, value)
    
    def get(self, username):
        """
        get value
        :param username: username
        :return:
        """
        return self.db.hget(self.name(), username)
    
    def delete(self, username):
        """
        delete key-value
        :param username: username
        :return: result
        """
        return self.db.hdel(self.name(), username)
    
    def count(self):
        """
        get count
        :return: count
        """
        return self.db.hlen(self.name())
    
    def random(self):
        """
        get random cookies or password
        :return: random cookies or password
        """
        return random.choice(self.db.hvals(self.name()))
    
    def usernames(self):
        """
        get all usernames
        :return: all usernames
        """
        return self.db.hkeys(self.name())
    
    def all(self):
        """
        get all key-values
        :return: map of key-values
        """
        return self.db.hgetall(self.name())
