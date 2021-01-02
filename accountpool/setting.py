import platform
from os.path import dirname, abspath, join
from environs import Env
from loguru import logger
from accountpool.utils.parse import parse_redis_connection_string

env = Env()
env.read_env()

# definition of flags
IS_WINDOWS = platform.system().lower() == 'windows'

# definition of dirs
ROOT_DIR = dirname(dirname(abspath(__file__)))
LOG_DIR = join(ROOT_DIR, env.str('LOG_DIR', 'logs'))

# definition of environments
DEV_MODE, TEST_MODE, PROD_MODE = 'dev', 'test', 'prod'
APP_ENV = env.str('APP_ENV', DEV_MODE).lower()
APP_DEBUG = env.bool('APP_DEBUG', True if APP_ENV == DEV_MODE else False)
APP_DEV = IS_DEV = APP_ENV == DEV_MODE
APP_PROD = IS_PROD = APP_ENV == PROD_MODE
APP_TEST = IS_TEST = APP_ENV == TEST_MODE

# redis host
REDIS_HOST = env.str('REDIS_HOST', '127.0.0.1')
# redis port
REDIS_PORT = env.int('REDIS_PORT', 6379)
# redis password, if no password, set it to None
REDIS_PASSWORD = env.str('REDIS_PASSWORD', None)
# redis db, if no choice, set it to 0
REDIS_DB = env.int('REDIS_DB', 0)
# redis connection string, like redis://[password]@host:port or rediss://[password]@host:port/0
REDIS_CONNECTION_STRING = env.str('REDIS_CONNECTION_STRING', None)

if REDIS_CONNECTION_STRING:
    REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_DB = parse_redis_connection_string(REDIS_CONNECTION_STRING)

# redis hash table key name
REDIS_ACCOUNT_KEY = env.str('REDIS_ACCOUNT_KEY', 'accounts:%s')
REDIS_CREDENTIAL_KEY = env.str('REDIS_CREDENTIAL_KEY', 'credential:%s')

# integrated generator
GENERATOR_MAP = {
    'antispider6': 'Antispider6Generator',
    'antispider7': 'Antispider7Generator'
}

# integrated tester
TESTER_MAP = {
    'antispider6': 'Antispider6Tester',
    'antispider7': 'Antispider7Tester',
}

# definition of tester cycle, it will test every CYCLE_TESTER second
CYCLE_TESTER = env.int('CYCLE_TESTER', 600)
# definition of getter cycle, it will get proxy every CYCLE_GENERATOR second
CYCLE_GENERATOR = env.int('CYCLE_GENERATOR', 600)
GET_TIMEOUT = env.int('GET_TIMEOUT', 10)

# definition of tester
TEST_URL = env.str('TEST_URL', 'http://www.baidu.com')
TEST_TIMEOUT = env.int('TEST_TIMEOUT', 10)
TEST_BATCH = env.int('TEST_BATCH', 20)
# test url
TEST_URL_MAP = {
    'antispider6': 'https://antispider6.scrape.center/',
    'antispider7': 'https://antispider7.scrape.center/'
}

# definition of api
API_HOST = env.str('API_HOST', '0.0.0.0')
API_PORT = env.int('API_PORT', 6789)
API_THREADED = env.bool('API_THREADED', True)

# flags of enable
ENABLE_TESTER = env.bool('ENABLE_TESTER', True)
ENABLE_GENERATOR = env.bool('ENABLE_GENERATOR', True)
ENABLE_SERVER = env.bool('ENABLE_SERVER', True)

logger.add(env.str('LOG_RUNTIME_FILE', join(LOG_DIR, 'runtime.log')), level='DEBUG', rotation='1 week',
           retention='20 days')
logger.add(env.str('LOG_ERROR_FILE', join(LOG_DIR, 'error.log')), level='ERROR', rotation='1 week')
