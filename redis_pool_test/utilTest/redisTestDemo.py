import json
import datetime
import time

from redisConPool import redis_client
from dateutil.relativedelta import relativedelta

class ManipulateRedis:

#=================================================================管道操作方法=================================================================
    @staticmethod
    def setDcUsedByRedis(user_id, tid, increamed=0):
        """
            单人批量操作 dc_used
        """
        redisor = None
        chance = 10
        user_cache = dict()
        dc_used = 0 + increamed
        livetime = ManipulateRedis.judger_time_isOver_tenM()

        while chance >= 1:
            #time.sleep(0.5)
            chance -= 1
            try:
                print(f"thread {tid} start get redisor")
                redisor = ManipulateRedis.getRedisor(6)

                #print(f"thread {tid} get pipeline")
                pipe = redisor.pipeline(transaction=True)

                #print(f"thread {tid} start watch")
                pipe.watch(user_id)

                #print(f"thread {tid} start multi")
                pipe.multi()

                print(f"thread {tid} start get info")
                info = redisor.get(user_id)
                #print(f"thread {tid} get info ::: {info}")
                #print(f"thread {tid} deal info")
                if info:
                    user_cache = json.loads(info)
                    user_cache["dc_used"] = user_cache["dc_used"] + dc_used
                else:
                    user_cache["dc_used"] = dc_used
                
                #print(f"thread {tid} start set data")
                pipe.set(user_id, json.dumps(user_cache), ex=datetime.timedelta(seconds=livetime))

                #print(f"thread {tid} start execute")
                pipe.execute()

                chance = 0
            except Exception as e:
                print(f'thread {tid} {chance}次机会')
                print(e)
                if chance == 0:
                    print(e)
            finally:
                print(f"thread {tid} close redisor")
                redisor.close()
                pipe.reset()
                pipe.close()
                if chance == 0:
                    print(f"thread {tid} finish")
                    break

    @staticmethod
    def rollbackDcUsedByRedis(user_ids: list, tid, increamed=-1):
        chance = 1
        redisor = None

        while True:
            print(f"thread {tid} start get redisor")
            redisor = ManipulateRedis.getRedisor(6)

            print(f"thread {tid} start get livetime")
            livetime = ManipulateRedis.judger_time_isOver_tenM()
            
            print(f"thread {tid} start get pipe")
            pipe = redisor.pipeline(transaction=True)

            try:
                print(f"thread {tid} start watch")
                pipe.watch(*user_ids)

                print(f"thread {tid} start multi")
                pipe.multi()

                print(f"thread {tid} start get infos")
                for key in user_ids:
                    info = json.loads(redisor.get(key))
                    info["dc_used"] += increamed
                    pipe.set(key, json.dumps(info),ex=datetime.timedelta(seconds=livetime))
                    
                pipe.execute()
                chance = 0
                print(f"thread {tid} finish")
            except Exception as e:
                #chance -= 1
                print(f'thread {tid} rollbackDcUsedByRedis异常:{str(e)}')
            finally:
                print(f"thread {tid} close redisor")
                redisor.close()
                pipe.reset()
                pipe.close()
                if chance == 0:
                    break

#=================================================================数据处理方法=================================================================

#=================================================================便捷工具方法=================================================================
    @staticmethod
    def getRedisor(db_num):
        redisor = None
        while True:
            try:
                #time.sleep(0.1)
                redisor =  redis_client.get_redis_db(db_num)
                if redisor.ping():
                    return redisor
            except Exception as e:
                continue

    @staticmethod
    def judger_time_isOver_tenM():
        """ 判断当前时间点距离下个月月初之前，时间是否超过10分钟
        """

        now = datetime.datetime.now()
        user_time = now

        # 获取下个月的第一天
        next_month = now + relativedelta(months=1)
        next_month_first_day = next_month.replace(day=1)

        # 获取下个月的第一天零点节点
        next_month_first_day_zero = next_month_first_day.replace(hour=0, minute=00, second=00)

        reference_time = next_month_first_day_zero

        #计算时间差
        time_diff = abs(reference_time - user_time)
        #如果时间差为10分钟以内（不包含10），就返回差值（秒），否则就返回10
        if time_diff <= datetime.timedelta(minutes=10):
            total_seconds = time_diff.total_seconds()
            return total_seconds
        else:
            return 1800
        