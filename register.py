import argparse
from acinonyx import run
import requests
from loguru import logger

parser = argparse.ArgumentParser(description='AccountPool')
parser.add_argument('website', type=str, help='website')
args = parser.parse_args()
website = args.website


@logger.catch()
def register(username, password):
    logger.debug(f'register using {username} and {password}')
    response = requests.post('https://antispider7.scrape.center/api/register', json={
        'username': username,
        'password': password
    })
    print(response.json())


accounts = []
for index in range(1, 1000):
    accounts.append((f'admin{index}', f'admin{index}'))
print(accounts)

run(register, accounts)
