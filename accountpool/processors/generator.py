from accountpool.exceptions.init import InitException
from accountpool.storages.redis import RedisClient
from loguru import logger


class BaseGenerator(object):
    def __init__(self, website=None):
        """
        init base generator
        :param website: name of website
        """
        self.website = website
        if not self.website:
            raise InitException
        self.account_operator = RedisClient(type='account', website=self.website)
        self.credential_operator = RedisClient(type='credential', website=self.website)
    
    def generate(self, username, password):
        """
        generate method
        :param username: username
        :param password: password
        :return:
        """
        raise NotImplementedError
    
    def init(self):
        """
        do init
        """
        pass
    
    def run(self):
        """
        run main process
        :return:
        """
        self.init()
        logger.debug('start to run generator')
        for username, password in self.account_operator.all().items():
            if self.credential_operator.get(username):
                continue
            logger.debug(f'start to generate credential of {username}')
            self.generate(username, password)


import requests


class Antispider6Generator(BaseGenerator):
    
    def init(self):
        """
        do init
        """
        if self.account_operator.count() == 0:
            self.account_operator.set('admin', 'admin')
            self.account_operator.set('admin2', 'admin2')
    
    def generate(self, username, password):
        """
        generate main process
        """
        if self.credential_operator.get(username):
            logger.debug(f'credential of {username} exists, skip')
            return
        login_url = 'https://antispider6.scrape.center/login'
        s = requests.Session()
        s.post(login_url, data={
            'username': username,
            'password': password
        })
        result = []
        for cookie in s.cookies:
            print(cookie.name, cookie.value)
            result.append(f'{cookie.name}={cookie.value}')
        result = ';'.join(result)
        logger.debug(f'get credential {result}')
        self.credential_operator.set(username, result)


class Antispider7Generator(BaseGenerator):

    MAX_COUNT = 100

    def init(self):
        """
        do init
        """
        for i in range(1, self.MAX_COUNT + 1):
            self.account_operator.set(f'admin{i}', f'admin{i}')

    def generate(self, username, password):
        """
        generate main process
        """
        if self.credential_operator.get(username):
            logger.debug(f'credential of {username} exists, skip')
            return
        login_url = 'https://antispider7.scrape.center/api/login'
        s = requests.Session()
        r = s.post(login_url, json={
            'username': username,
            'password': password
        })
        if r.status_code != 200:
            logger.error(f'error occurred while generating credential of {username}, error code {r.status_code}')
            return
        token = r.json().get('token')
        logger.debug(f'get credential {token}')
        self.credential_operator.set(username, token)
