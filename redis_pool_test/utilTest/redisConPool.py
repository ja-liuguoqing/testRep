import redis

from flask import Flask

app = Flask(__name__)

#怎么放
HOST = app.config.get("CACHE_REDIS_HOST","127.0.0.1")
PORT = app.config.get("CACHE_REDIS_PORT","6379")
PASSWORD = app.config.get("CACHE_REDIS_PASSWORD","123456")
MAX_CON = 15
connects = (1, 5, 6)
class RedisClient:
    def __init__(self):
        try:
            # 拿到一个Redis实例的连接池，避免每次建立、释放连接的开销，节省了每次连接用的时间
            self._connectList = [None for _ in range(16)]
            for db_index in connects:
                self._connectList[db_index] = redis.ConnectionPool(
                                                host=HOST, port=PORT, decode_responses=True, db=db_index, password=PASSWORD, max_connections=MAX_CON
                                            )
        except Exception as e:
            print(f'获取新Redis连接池异常, 程序退出:{str(e)}')#traceback={traceback.format_exc()}')
    def get_redis_db(self, db_num):
        redis_conn = None
        try:
            # 从连接池中获取一个连接实例
            redis_conn = redis.StrictRedis(connection_pool=self._connectList[db_num])
            if redis_conn.ping():
                print(f'Redis连接成功:{db_num}')
            return redis_conn
        except Exception as e:
            return None
            #app.logger.error(f'Redis连接异常:{str(e)}')#,traceback={traceback.format_exc()}')

redis_client = RedisClient()