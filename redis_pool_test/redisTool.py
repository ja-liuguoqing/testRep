import json

from redisConPool import redis_client

USER_USED_KEY = "z_recordForDcOfUserIsDict"
redisor = redis_client.get_redis_db(5)
KEY_LEN = 40
#过滤数据，保留 task
def filter_data():
    cursor = '0'
    while cursor != 0:
        cursor, keys = redisor.scan(cursor=cursor)
        for key in keys:
            print(key)
            print(redisor.get(key))