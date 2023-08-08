import json
import datetime
import time
import redis

from dateutil.relativedelta import relativedelta

USER_USED_KEY = "z_recordForDcOfUserIsDict"

#===================================================================查询数据处理方法===================================================================

def setDcUsedByRedis(redisor, user_id, increamed):
    """ 
        用户下载任务，次数修正
    """

    dc_used = 0 + increamed
    flag = False
    current_user = None
    counts = 0
    pipe = redisor.pipeline(transaction=True)

    while True:
        flag, current_user = queryExistUserByUserId(redisor, user_id)
        try:
            pipe.watch(USER_USED_KEY)
            pipe.multi()
            if flag:
                dc_used = current_user[0] + increamed
                timestamp = current_user[1]
                new_timestamp, ts = delUInfoInRedisIsExp(timestamp)
                pipe.zremrangebyscore(USER_USED_KEY, ts, new_timestamp)

            userInfo, now_timestamp, livetime = insertUserInfo(user_id, dc_used)
            pipe.zadd(USER_USED_KEY, {userInfo: now_timestamp})
            pipe.expire(USER_USED_KEY, datetime.timedelta(seconds=livetime))
            pipe.execute()
            redisor.close()
            break
        except redis.WatchError as e:
            counts += 1
            continue
#===================================================================redis操作方法===================================================================

def insertUserInfo(user_id, dc_used):
    """
        redis 的 z-set 插入数据之前，建议先执行删除
    """

    timestamp = int(time.time())
    userInfo = json.dumps({user_id : dc_used})
    livetime = judger_time_isOver_tenM()
    return userInfo, timestamp, livetime

def delUInfoInRedisIsExp(timestamp = 'inf'):
    """
        当 timestamp != inf 时，则只能是一个时间戳数值，此时是根据时间戳删除对应的某一个具体用户信息
        反之则是删除过期的用户信息
    """
    ts = '-inf'
    if timestamp != 'inf':
        ts = timestamp
    else:
        timestamp = int(time.time()) - 1800 #若时间戳为默认值，则删除，以当前时间点  往前推30分钟，在那个时间点之前的所有数据都将被删除
    return timestamp, ts

def queryExistUserByUserId(redisor, user_id):
    """
        根据 user_id 查询用户信息。
        查到返回 true 和 对应的用户信息；没查到返回 false 和 None
    """

    flag = False
    current_user = None
    userListInRedis = None

    members = (redisor.zrangebyscore(USER_USED_KEY, '-inf', '+inf', withscores=True)) # 获取所有成员

    if len(members):#redis does not store info
        userListInRedis = unTupleGetUserid(members)
        current_user = userListInRedis.get(user_id)

    if current_user:
        flag = True

    return flag, current_user

def queryExistUserByUserIdlist(redisor, user_ids):
    exit_user = dict()
    not_exit_user = list()

    members = (redisor.zrangebyscore(USER_USED_KEY, '-inf', '+inf', withscores=True)) # 获取所有成员

    if len(members):#redis does not store info
        userListInRedis = unTupleGetUserid(members)
        for user_id in user_ids:
            user = userListInRedis.get(user_id)
            if user:
                exit_user[user_id] = user
            else:
                not_exit_user.append(user_id)
    else:
        not_exit_user = user_id

    return exit_user, not_exit_user


#===================================================================工具方法===================================================================

def unTupleGetUserid(t_b_d):
    """
        将传入的元组中的数据，拆包成需要的数据
    """
    res_dict = dict()#结果包
    for t in t_b_d:
        timestamp = int(t[1])#时间
        dict_date = json.loads(t[0])#数据字典
        for k, v in dict_date.items():#解包装包
            i = [v, timestamp]
            res_dict[k] = i
    return res_dict

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