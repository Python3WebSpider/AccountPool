from accountpool.storages.redis import RedisClient

conn = RedisClient('account', 'antispider7')
start = 1
end = 100
for i in range(start, end + 1):
    username = password = f'admin{i}'
    conn.set(username, password)
