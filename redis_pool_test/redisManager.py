import json

from redisConPool import redis_client

USER_USED_KEY = "z_recordForDcOfUserIsDict"
redisor = redis_client.get_redis_db(5)

cursor = '0'
while cursor != 0:
    cursor, keys = redisor.scan(cursor=cursor)
    for key in keys:
        print(f"key-value：{key}+++key-len：{len(key)}")