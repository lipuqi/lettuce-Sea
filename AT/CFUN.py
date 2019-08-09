import time
import re


class CFUN:

    def __init__(self, serialPort, receiveMsg):
        super(CFUN, self).__init__()
        self.serialPort = serialPort
        self.receiveMsg = receiveMsg
        self.at_name = "CFUN"
        self.at_error_result = None
        self.at_suc_result = None
        self.status = 0
        self.at_result_pattern = None
        self.retry = 1

    def query_at(self, data=None):
        print("查询射频情况")
        self.serialPort.write_data(self.at_name, "?", data)
        self.at_result_pattern = re.compile(self.at_name)
        self.receiveMsg.atObj = self
        self.status = 0
        time.sleep(1)
        while True:
            if self.retry == 4:
                print("执行失败，不再重试")
                self.retry = 1
                return 2
            if self.status == 1:
                print("执行成功")
                self.retry = 1
                return 1
            elif self.status == 2:
                print("执行失败，重试" + str(self.retry))
                self.retry += 1
                time.sleep(2)
                return self.query_at(data)

    def execute_at(self, data=None):
        print("执行射频设置")
        self.serialPort.write_data(self.at_name, "=", data)
        self.at_suc_result = data
        self.receiveMsg.atObj = self
        self.status = 0
        time.sleep(1)
        while True:
            if self.retry == 4:
                print("执行失败，不再重试")
                self.retry = 1
                return 2
            if self.status == 1:
                print("执行成功")
                self.retry = 1
                return 1
            elif self.status == 2:
                print("执行失败，重试" + str(self.retry))
                self.retry += 1
                time.sleep(2)
                return self.execute_at(data)

    def update_status(self, sta):
        self.status = sta
