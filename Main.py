import threading
from common import *
from Running_manage import Running_manage
from Model_manage import Model_manage
from Listener_manage import Listener_manage
from model.core_model.core_m import core_m
from job.Job_manage import Job_manage
import time

log = Logger().logger


def quit_sys():
    time.sleep(60 * 10)
    if mm.current_connect_model.access_idle():
        if mm.current_connect_model.quit_nb():
            rm.read_data_thread_quit = True
            rm.new_message_quit = True
            rm.send_message_quit = True
            rm.inform_quit = True
            jm.scheduler.shutdown()


if __name__ == '__main__':
    log.info("----主线程启动----")
    rm = Running_manage()
    mm = Model_manage(rm)
    core = core_m(rm, mm)
    lm = Listener_manage(rm, mm, core)

    log.info("----开始启动通信模块，消息处理模块监听----")
    connect_model = threading.Thread(target=lm.listener_connect_model)
    inform = threading.Thread(target=lm.listener_inform)
    send_message = threading.Thread(target=lm.listener_send_message)
    connect_model.start()
    send_message.start()
    inform.start()

    log.info("----开始启动通信模块初始化----")
    if mm.current_connect_model.init():
        new_message = threading.Thread(target=lm.listener_new_message)
        new_message.start()
        log.info("----通信模块初始化成功----")
        jm = Job_manage(mm, core)
        quit_sys()
    else:
        log.info("----通信模块初始化失败----")
        rm.read_data_thread_quit = True
        rm.new_message_quit = True
        rm.send_message_quit = True
        rm.inform_quit = True

