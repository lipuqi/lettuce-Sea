import threading
from common import *
from Running_manage import Running_manage
from Model_manage import Model_manage
from Listener_manage import Listener_manage
from model.core_model.core_m import core_m
from job.Job_manage import Job_manage
import time

log = Logger().logger

rm = None
mm = None
core = None
lm = None
jm = None


def start_sys():
    global rm, mm, core, lm, jm
    log.info("----主线程启动----")
    rm = Running_manage()
    mm = Model_manage(rm)
    core = core_m(rm, mm)
    lm = Listener_manage(rm, mm, core)
    log.info("----开始启动通信模块，消息处理模块监听----")
    threading.Thread(target=lm.listener_connect_model).start()
    threading.Thread(target=lm.listener_inform).start()
    threading.Thread(target=lm.listener_send_message).start()

    log.info("----开始启动通信模块初始化----")
    if mm.current_connect_model.init():
        threading.Thread(target=lm.listener_new_message).start()
        log.info("----通信模块初始化成功----")
        jm = Job_manage(mm, core)
    else:
        log.info("----通信模块初始化失败----")


def quit_sys():
    global rm, mm, core, lm, jm
    rm.quit()
    mm.quit()
    core.quit_model()
    jm.scheduler.shutdown()
    rm = None
    mm = None
    core = None
    lm = None
    jm = None


if __name__ == '__main__':
    start_sys()
    time.sleep(5 * 60)
    quit_sys()

