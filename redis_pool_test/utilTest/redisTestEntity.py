import threading
import time
import datetime
import json

from redisTestDemo import ManipulateRedis

class ThreadTestAdd(threading.Thread):

    def __init__(self, user_id, tid, increamed=0):
        super().__init__()
        self.user_id = user_id
        self._thread_ids = tid
        self.incramed = increamed
    
    def run(self) -> None:
        print(f"Thread {self._thread_ids} started")

        ManipulateRedis.setDcUsedByRedis(self.user_id, self._thread_ids, self.incramed)

        print(f"Thread {self._thread_ids} finished")

class ThreadTestDec(threading.Thread):

    def __init__(self, user_ids:list, tid):
        super().__init__()
        self._thread_ids = tid
        self.user_ids = user_ids
    
    def run(self) -> None:
        print(f"Thread {self._thread_ids} started")

        ManipulateRedis.rollbackDcUsedByRedis(self.user_ids, self._thread_ids)

        print(f"Thread {self._thread_ids} finished")

user_ids = (
"8361b978fad611edabd402420a000028",
"a1722a82b09611ec843c0242ac170003",
"9549c2540be611ee8f3d02420a000089",
"178d130a244411ed9e570242ac170004",
"bd145d32b24911ec96940242ac170004",
"08c073ee37fe11eda8820242ac170004",
"20cebf4e334511ed8ba30242ac170004",
"de5cdba40c1611ee983a02420a000089",
"a75a5e64d77f11ecb3660242ac170004",
"6fa68b745f4611ed9daa0242ac170004",
"170c6440149e11ed86ea0242ac170004",
"5bb08aae512a11edb1f30242ac170004",
"41834d50bfe011eca4ec0242ac170004",
"99bd5eb6b34c11ec808c0242ac170004",
"e252475ae28411ed8e0702420a000028",
"07f03d704b8911edabbd0242ac170004",
"7770139e0c1a11ee908802420a00008a",
"c83c027437e511ed807b0242ac170004",
"3bbba6fc49d211eda8a10242ac170004",
"49d9153e3e3411edb2850242ac170004",
"ca6e3fe079c511ed992d0242ac170004",
"67ad83d01c6d11edb6910242ac170004",
"3848bca00f3c11ee808002420a00008a",
"4251a1700f3d11eea96c02420a000089",
"6152d75238be11eda5d30242ac170004",
"bfb20aeab24d11ec96940242ac170004",
"6c1d8bec0f4011eea96c02420a000089",
"1ba4f0820f4111eeaf1302420a000089",
"ea66deac0f4211eeba5d02420a00008a",
"0b6ab10c494911ed96200242ac170004",
"61ae03cc0f4411eea96c02420a000089",
"1a010ab40f4511eeaf1302420a000089",
"0103131cf82211ec82860242ac170004",
"0348e118178c11ed86040242ac170004",
"47b54a8eeb8711eca90f0242ac170004",
"36c8d3f80f4911eeba5d02420a00008a",
"db61a8bc0f4a11eea96c02420a000089",
"2547ddf60f4c11eea96c02420a000089",
"357fb07c0f4c11eea94c02420a00008a",
"3f56e7ca0f4f11eea94c02420a00008a",
"b97233400fd411eeba5d02420a00008a",
"5d72c98e380111ed99c80242ac170004",
"51f8b7f0100811eea88902420a00008a",
"fce321d4fdcb11eda7752cdb07319911",
"3f537cf4fdcc11edb00f2cdb07319911",
"28e179ca134a11eeb1cf02420a000089",
"e1fa32c638b711edaa5f0242ac170004",
"1e89a54013f611ee824e02420a000089",
"1f5753ae13f711ee824e02420a000089",
"78b7a55c140111ee92d702420a0000eb",
"77dccca6064811edb7860242ac170004",
"9b3850f637c311edb29d0242ac170004",
"09f340ac149911ee92d702420a0000eb",
"9438d7d02ab211edaebf0242ac170004",
"a6abb596bc9d11ec8e3c0242ac170004",
"5ef679a816af11eeaf9c02420a00001d",
"f621723e197411eeab4b02420a00000e",
"19fce1b42e6311edb8560242ac170004",
"b3db8c1ebfae11ec9cef0242ac170004",
"8a9ff3281cc611ee9c0102420a000078",
"164c9fe81ccc11ee9c1602420a000078",
"6d7ee5e2cd2111ec8c770242ac170004",
"1382c4a21ef411eeb28f02420a00007a",
"35cfff261ef811eeb28f02420a00007a",
"121a26661f0b11eea05f02420a000078",
"d704fb1c1fb111eeb28f02420a00007a",
"a955ff661fd611eead9e02420a00007a",
"b422bf721eed11eeb28f02420a00007a",
"eaff6dac213011eea55102420a00007a",
"4387f6ae246c11eeb48202420a00007a",
"e84ccf98247111eeb76202420a000078",)

#max = len(user_ids)
max = 1

threads = []
# 创建10个线程
for i in range(0, max, 1):
    #t = ThreadTestAdd(user_ids[i], i+1, 1)
    t = ThreadTestDec(user_ids,i+1)
    threads.append(t)

print(f"All threads started")
# 启动线程
for t in threads:
    t.start()

# 等待所有线程完成
for t in threads:
    t.join()
print("All threads finished")