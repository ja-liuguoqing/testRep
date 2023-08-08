import threading
import time
import datetime
import json

from redisConPool import redis_client
from redisMapper import setDcUsedByRedis

class ThreadTest(threading.Thread):

    def __init__(self, user_id='m', increamed=0):
        super().__init__()
        self.user_id = user_id
        self.incramed = increamed
    
    def run(self) -> None:
        print(f"Thread {self.user_id} started")
        redisor = None
        counts = 1
        while not redisor:
            try:
                time.sleep(0.1)
                redisor = redis_client.get_redis_db(5)
            except Exception as e:
                continue
        print(f"redis doing ::: {self.user_id} is fast")
        m = 1
        """

        while m>=0:
            setDcUsedByRedis(redisor, self.user_id, self.incramed)
            self.incramed = 1
            m -= 1
            time.sleep(1)
        """
        setDcUsedByRedis(redisor, self.user_id, self.incramed)

        print(f"Thread {self.user_id} finished")
        

# 创建并启动十个线程
t_name = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
          'aa','ab','ac','ad','ae','af','ag','ah','ai','aj','ak','al','am','an','ao','ap','aq','ar','as','at','au','av','aw','ax','ay','az',
          'ba','bb','bc','bd','be','bf','bg','bh','bi','bj','bk','bl','bm','bn','bo','bp','bq','br','bs','bt','bu','bv','bw','bx','by','bz',
          'ca','cb','cc','cd','ce','cf','cg','ch','ci','cj','ck','cl','cm','cn','co','cp','cq','cr','cs','ct','cu','cv','cw','cx','cy','cz',]
threads = []

"""
print(f"initialize")

#r = redis_client.get_redis_db(5)
#r.close()
# 创建10个线程
for i in range(0, 100, 1):
    t = ThreadTest(t_name[i], i)
    threads.append(t)

print(f"All threads started")
# 启动线程
print(f"threads ::: {len(threads)}")
for t in threads:
    t.start()

# 等待所有线程完成
for t in threads:
    t.join()
print("All threads finished")

"""
redisor = redis_client.get_redis_db(5)
pipe = redisor.pipeline(transaction=True)
keys = list()
keys2 = list()
for i in range(0, 100, 1):
    pipe.set(t_name[i], json.dumps({"dc_used":i}), ex=datetime.timedelta(days=3))
"""
for i in range(0, 100, 1):
    keys.append(t_name[i])
pipe.watch(*keys)
pipe.multi()
res = redisor.mget(keys)
print(type(json.loads(res[0])))
print(res)
for i, key in enumerate(keys):
    data = json.loads(res[i])
    data['dc_used'] = 0
    pipe.set(key, json.dumps(data),ex=datetime.timedelta(days=3))
"""

pipe.execute()
redisor.close()
pipe.reset()
pipe.close()