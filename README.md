# AccountPool

![build](https://github.com/Python3WebSpider/AccountPool/workflows/build/badge.svg)
![](https://img.shields.io/badge/python-3.6%2B-brightgreen)
![Docker Pulls](https://img.shields.io/docker/pulls/germey/accountpool)

简易高效的账号池，提供如下功能：

* 定时模拟登录账号，将 Cookies 或 JWT 等信息存储到 Redis 数据库。
* 定时测试，剔除不可用 Cookies 或 JWT。
* 提供 API，随机取用测试通过的可用 Cookies 或 JWT。

## 使用要求

可以通过两种方式来运行账号池，一种方式是使用 Docker（推荐），另一种方式是常规方式运行。

### Docker

如果使用 Docker，则需要安装如下环境：

* Docker
* Docker-Compose

### 常规方式

常规方式要求有 Python 环境、Redis 环境，具体要求如下：

* Python>=3.6
* Redis

## Docker 运行

如果安装好了 Docker 和 Docker-Compose，只需要一条命令即可运行。

```shell script
docker-compose up
```

运行结果类似如下：

```
redis          | 1:C 09 Oct 2020 18:20:13.963 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
redis          | 1:C 09 Oct 2020 18:20:13.963 # Redis version=6.0.8, bits=64, commit=00000000, modified=0, pid=1, just started
redis          | 1:M 09 Oct 2020 18:20:13.964 * RDB memory usage when created 0.83 Mb
redis          | 1:M 09 Oct 2020 18:20:13.964 * DB loaded from disk: 0.000 seconds
redis          | 1:M 09 Oct 2020 18:20:13.964 * Ready to accept connections
accountpool    | 2020-10-09 18:20:14,089 CRIT Supervisor is running as root.  Privileges were not dropped because no user is specified in the config file.  If you intend to run as root, you can set user=root in the config file to avoid this message.
accountpool    | 2020-10-09 18:20:14,091 INFO supervisord started with pid 1
accountpool    | 2020-10-09 18:20:15,094 INFO spawned: 'generator' with pid 9
accountpool    | 2020-10-09 18:20:15,096 INFO spawned: 'server' with pid 10
accountpool    | 2020-10-09 18:20:15,098 INFO spawned: 'tester' with pid 11
accountpool    | 2020-10-09 18:20:16,280 INFO success: generator entered RUNNING state, process has stayed up for > than 1 seconds (startsecs)
accountpool    | 2020-10-09 18:20:16,280 INFO success: server entered RUNNING state, process has stayed up for > than 1 seconds (startsecs)
accountpool    | 2020-10-09 18:20:16,280 INFO success: tester entered RUNNING state, process has stayed up for > than 1 seconds (startsecs)
```

可以看到 Redis、Generator、Server、Tester 都已经启动成功。

另外还需要导入一些账号信息到 Redis 数据库里面，由于已经用 Docker 启动了 Redis 数据库，运行在 6333 端口上。

这时候可以执行脚本：

```
export REDIS_PORT=6333
python3 importer.py antispider7
```

运行完成之后如果没有报错就说明账号导入成功了，可以自行连上 Redis 看下。

过一会访问 [http://localhost:6777/antispider7/random](http://localhost:6777/antispider7/random) 即可获取一个 [antispider7](https://antispider7.scrape.center) 的随机可用 Cookies。

## 常规方式运行

如果不使用 Docker 运行，配置好 Python、Redis 环境之后也可运行，步骤如下。

### 安装和配置 Redis

本地安装 Redis、Docker 启动 Redis、远程 Redis 都是可以的，只要能正常连接使用即可。

首先可以需要一下环境变量，代理池会通过环境变量读取这些值。

设置 Redis 的环境变量有两种方式，一种是分别设置 host、port、password，另一种是设置连接字符串，设置方法分别如下：

设置 host、port、password，如果 password 为空可以设置为空字符串，示例如下：

```shell script
export REDIS_HOST='localhost'
export REDIS_PORT=6379
export REDIS_PASSWORD=''
export REDIS_DB=0
```

或者只设置连接字符串：

```shell script
export REDIS_CONNECTION_STRING='redis://[password]@host:port/db'
```

如果没有密码也要设置为：

```shell script
export REDIS_CONNECTION_STRING='redis://@host:port/db'
```

这里连接字符串的格式需要符合 `redis://[password]@host:port/db` 的格式，注意不要遗漏 `@`。

以上两种设置任选其一即可。

### 安装依赖包

这里强烈推荐使用 [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands) 
或 [virtualenv](https://virtualenv.pypa.io/en/latest/user_guide.html) 创建虚拟环境，Python 版本不低于 3.6。

然后 pip 安装依赖即可：

```shell script
pip3 install -r requirements.txt
```

### 运行代理池

两种方式运行账号池，一种是 Tester、Generator、Server 全部运行，另一种是按需分别运行。

一般来说可以选择全部运行，命令如下：

```shell script
python3 run.py <website>
```

运行之后会启动 Tester、Generator、Server，这时访问 [http://localhost:6777/<website>/random](http://localhost:6777/<website>/random) 即可获取一个随机可用代理。

或者如果你弄清楚了账号池的架构，可以按需分别运行，命令如下：

```shell script
python3 run.py <website> --processor getter
python3 run.py <website> --processor tester
python3 run.py <website> --processor server
```

这里 processor 可以指定运行 Tester、Generator 还是 Server。

## 可配置项

账号池可以通过设置环境变量来配置一些参数。

### 开关

* ENABLE_TESTER：允许 Tester 启动，默认 true
* ENABLE_GENERATOR：允许 Generator 启动，默认 true
* ENABLE_SERVER：运行 Server 启动，默认 true

### 环境

* APP_ENV：运行环境，可以设置 dev、test、prod，即开发、测试、生产环境，默认 dev
* APP_DEBUG：调试模式，可以设置 true 或 false，默认 true

### Redis 连接

* REDIS_HOST：Redis 的 Host
* REDIS_PORT：Redis 的端口
* REDIS_PASSWORD：Redis 的密码
* REDIS_DB：Redis 的数据库索引，如 0、1
* REDIS_CONNECTION_STRING：Redis 连接字符串
* REDIS_KEY：Redis 储存代理使用字典的名称

### 处理器

* CYCLE_TESTER：Tester 运行周期，即间隔多久运行一次测试，默认 20 秒
* CYCLE_GETTER：Getter 运行周期，即间隔多久运行一次代理获取，默认 100 秒
* API_HOST：代理 Server 运行 Host，默认 0.0.0.0
* API_PORT：代理 Server 运行端口，默认 6777
* API_THREADED：代理 Server 是否使用多线程，默认 true

### 日志

* LOG_DIR：日志相对路径
* LOG_RUNTIME_FILE：运行日志文件名称
* LOG_ERROR_FILE：错误日志文件名称

## 部署

本项目提供了 Kubernetes 部署脚本，如需部署到 Kubernetes，执行如下命令即可：

```shell script
cat deployment.yml | sed 's/\${TAG}/latest/g' | kubectl apply -f -
```

## 待开发

- [ ] 前端页面管理
- [ ] 使用情况统计分析

如有一起开发的兴趣可以在 Issue 留言，非常感谢！

## LICENSE

MIT
