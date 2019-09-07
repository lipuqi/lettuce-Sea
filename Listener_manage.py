from model import *
from common import *

# ------------------------------------------------------------------------------
# 监听管理
# ------------------------------------------------------------------------------

log = Logger().logger


class Listener_manage:
    def __init__(self, running_manage, model_manage, core_m):
        self.rm = running_manage
        self.mm = model_manage
        self.core_model = core_m

    def listener_connect_model(self):
        while not self.rm.read_data_thread_quit:
            while self.rm.read_data_thread_pause:
                pass
            self.mm.current_connect_model.read_data()

    def listener_new_message(self):
        while not self.rm.new_message_quit:
            while self.rm.new_message_pause:
                pass
            if not self.rm.new_message.empty():
                new_message = self.rm.new_message.get()
                model, command_name, params = decode.Decode(new_message[2:], self.core_model.conf,
                                                            self.mm.current_model.conf).parse_data()
                if model == 0:
                    self.core_model.main(command_name, params=params)
                else:
                    self.mm.current_model.main(command_name, params=params)

    def listener_send_message(self):
        while not self.rm.send_message_quit:
            while self.rm.send_message_pause:
                pass
            if not self.rm.send_message.empty():
                send_message = self.rm.send_message.get()
                if not self.mm.current_connect_model.send_msg(send_message):
                    log.error("发送信息失败" + send_message)

    def listener_inform(self):
        while not self.rm.inform_quit:
            while self.rm.inform_pause:
                pass
            if not self.rm.inform.empty():
                inform = self.rm.inform.get()
                if inform == "3":
                    log.info("已经与云平台连接成功")



