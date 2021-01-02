import argparse
from acinonyx import run
import requests
from loguru import logger

# This is a script for registering account for antispider7, using acinonyx to accelerate.

parser = argparse.ArgumentParser(description='AccountPool')
parser.add_argument('website', type=str, help='website')
args = parser.parse_args()
website = args.website


@logger.catch()
def register(username, password):
    logger.debug(f'register using {username} and {password}')
    response = requests.post(f'https://{website}.scrape.center/api/register', json={
        'username': username,
        'password': password
    })
    print(response.json())


if __name__ == '__main__':
    accounts = []
    for index in range(1, 1000):
        accounts.append((f'admin{index}', f'admin{index}'))
    run(register, accounts)
