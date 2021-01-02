from accountpool.storages.redis import RedisClient
import argparse

parser = argparse.ArgumentParser(description='AccountPool')
parser.add_argument('website', type=str, help='website')
args = parser.parse_args()
website = args.website

conn = RedisClient('account', args.website)
start = 1
end = 100
for i in range(start, end + 1):
    username = password = f'admin{i}'
    conn.set(username, password)
