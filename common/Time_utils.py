import time
import datetime

# ------------------------------------------------------------------------------
# 时间工具
# ------------------------------------------------------------------------------


# 延时秒
def delay_s(s):
    time.sleep(s)


# 延时微秒
def delay_us(us):
    time.sleep(us * 1/1000/1000)


# 延时毫秒
def delay_ms(ms):
    time.sleep(ms * 1/1000)


# 获得当前时间
def get_now_time():
    return datetime.datetime.now()


class Time_utils:
    _format1 = '%Y-%m-%d %H:%M:%S'
    _format2 = '%Y-%m-%d %H:%M'
    _format3 = '%Y-%m-%d'

    def __init__(self, time_date=None):
        self._time_date = time_date

    def set_time_date(self, date):
        self._time_date = date

    # 获取时间差 微秒
    def diff_time_us(self, end_time):
        st = int(self._time_date.strftime('%f'))
        et = int(end_time.strftime('%f'))
        return (et - st) / 1000

