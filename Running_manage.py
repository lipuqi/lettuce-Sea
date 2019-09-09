from common.Log_utils import Logger
from queue import Queue

# ------------------------------------------------------------------------------
# 运行管理
# ------------------------------------------------------------------------------


class Running_manage:

    def __init__(self):
        self._pin_in_io = []  # io输入口占用列表
        self._pin_out_io = []  # io输出口占用列表
        self.new_message = Queue()  # 接收消息队列
        self.send_message = Queue()  # 发送消息队列
        self.upgrade = Queue()  # 升级消息队列
        self.inform = Queue()  # 平台通知队列

        self.execute_running_marking = 0  # 执行运行标识 0运行，1关闭， 2重启, 3无状态
        self.running_status = 0  # 运行状态 0运行中，1启动中，2退出中, 3退出成功，4无状态

        self.read_data_thread_quit = False
        self.read_data_thread_pause = False

        self.new_message_quit = False
        self.new_message_pause = False

        self.send_message_quit = False
        self.send_message_pause = False

        self.upgrade_quit = False
        self.upgrade_pause = False

        self.inform_quit = False
        self.inform_pause = False

    # 初始化输出端口
    def setup_out_io(self, out_io):
        if out_io in self._pin_out_io and out_io in self._pin_in_io:
            Logger().logger.error("指定输出io口失败，已经被占用")
            return False
        else:
            self._pin_out_io.append(out_io)
            return True

    # 初始化输入端口
    def setup_in_io(self, in_io):
        if in_io in self._pin_in_io and in_io in self._pin_out_io:
            Logger().logger.error("指定输入io口失败，已经被占用")
            return False
        else:
            self._pin_in_io.append(in_io)
            return True

    # 清除占用IO口
    def clear_pin(self, pin_ios):
        for ios in pin_ios:
            while ios in self._pin_in_io:
                self._pin_in_io.remove(ios)
            while ios in self._pin_in_io:
                self._pin_in_io.remove(ios)
