import re
import time


class NRB:

    def __init__(self, serialPort, receiveMsg):
        super(NRB, self).__init__()
        self.serialPort = serialPort
        self.receiveMsg = receiveMsg
        self.at_name = "NRB"
        self.at_error_result = None
        self.at_suc_result = None
        self.status = 0
        self.at_result_pattern = None
        self.retry = 1

    def execute_at(self, data=None):
        print("执行重启")
        self.receiveMsg.set_is_pause(1)
        self.serialPort.write_data(self.at_name, None, data)
        self.serialPort.port_close()
        time.sleep(3)
        self.serialPort.port_open()
        self.receiveMsg.atObj = self
        self.status = 0
        time.sleep(3)
        self.receiveMsg.set_is_pause(0)
        time.sleep(1)
        while True:
            if self.retry == 4:
                print("执行失败，不再重试")
                self.retry = 1
                return 2
            if self.status == 1:
                print("执行成功")
                self.retry = 1
                time.sleep(3)
                return 1
            elif self.status == 2:
                print("执行失败，重试" + str(self.retry))
                self.retry += 1
                time.sleep(2)
                return self.execute_at(data)

    def update_status(self, sta):
        self.status = sta
