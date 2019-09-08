import threading
from common import *
from Running_manage import Running_manage
from Model_manage import Model_manage
from Listener_manage import Listener_manage
from model.core_model.core_m import core_m
from job.Job_manage import Job_manage
import sys

log = Logger().logger

running = False

rm = Running_manage()
mm = None
core = None
lm = None
jm = None


def start_sys():
    global mm, core, lm, jm
    try:
        log.info("----主线程启动----")
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
            log.info("----主线程启动成功----")
            jm = Job_manage(mm, core)
            return True
        else:
            log.error("----通信模块初始化失败----")
            return False
    except:
        log.error("----主线程启动失败----")
        log.exception(sys.exc_info())
        return False


def quit_sys():
    global mm, core, lm, jm
    log.info("----执行退出流程----")
    try:
        if lm:
            lm.quit()
        if mm:
            mm.quit()
        if core:
            core.quit_model()
        if jm:
            jm.scheduler.shutdown()
        mm = None
        core = None
        lm = None
        jm = None
        log.info("----执行退出成功----")
        return True
    except:
        log.error("----执行退出失败----")
        log.exception(sys.exc_info())
        return False


if __name__ == '__main__':
    while True:
        if rm.execute_running_marking == 0 and not running:
            rm.running_status = 1
            if start_sys():
                running = True
                rm.running_status = 0
            else:
                log.info("----启动失败，进入退出流程----")
                rm.running_status = 3
                quit_sys()
                break
        if rm.execute_running_marking == 1 and running:
            rm.running_status = 3
            quit_sys()
            break
        if rm.execute_running_marking == 2 and running:
            rm.running_status = 3
            running = False
            if not quit_sys():
                break
            else:
                rm.execute_running_marking = 0
