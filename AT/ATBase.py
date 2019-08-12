import time
import re

"""
AT基础类
所有AT的父类
"""


class ATBase:

    def __init__(self, serialPort, receiveMsg):
        self.serialPort = serialPort  # 串口基础操作模块
        self.receiveMsg = receiveMsg  # 串口数据接收模块
        self.at_name = ""  # AT指令名称
        self.at_error_result = None  # AT指令返回信息校验（错误结果）
        self.at_suc_result = None  # AT指令返回信息校验（正确结果）
        self.status = 0  # 执行结果（0未执行1执行成功2执行失败）
        self.at_result_pattern = None  # 匹配返回结果的正则类型
        self.error = re.compile('ERROR')  # 普通消息失败
        self.ok = re.compile('OK')  # 普通消息成功
        self.result = None  # 执行结果
        self.retry = 3  # 重试次数

    # 发送at基础方法
    def send_at(self, data=None, at_type=None):
        retry = self.retry
        self.serialPort.write_data(self.at_name, data, at_type)  # 调用串口基础操作-写入
        self.receiveMsg.atObj = self  # 将本类基本信息注入串口数据接收以便更新执行情况
        self.status = 0  # 复位执行结果
        time.sleep(1)
        # 执行写入以后，主程序阻塞等待执行结果
        while True:
            if self.retry == 0:
                print("执行失败，不再重试")
                self.retry = retry
                self.off_compile_result()  # 自动复位
                return 2
            if self.status == 1:
                print("执行成功")
                self.retry = retry
                self.off_compile_result()  # 自动复位
                return 1
            elif self.status == 2:
                print("执行失败，重试" + str(4 - self.retry))
                self.retry -= 1
                time.sleep(2)
                return self.send_at(data, at_type)  # 执行失败后递归调用

    # 查询指令
    def query_at(self):
        return self.send_at("?")

    # 执行指令
    def execute_at(self, data=None):
        if data:
            return self.send_at("=", data)
        return self.send_at()

    # 校验返回结果
    def compile_result(self, result):
        # 有关键字正则表示需要结果校验，没有则只判断成功/失败
        if self.at_result_pattern:
            if self.at_result_pattern.search(result):
                at_result = result.split(":")
                if self.at_error_result:
                    self.status = self.compile_error_result(at_result[1])
                    print(result)
                elif self.at_suc_result:
                    self.status = self.compile_suc_result(at_result[1])
                    print(result)
        else:
            if self.ok.search(result):
                self.status = 1
                print(result)
                return True
            elif self.error.search(result):
                self.status = 2
                print(result)
                return True
        return False  # 返回 True/False是因为表示指令执行成功

    # 开启错误校验结果
    def on_compile_error_result(self, error):
        self.at_result_pattern = re.compile(self.at_name)
        self.at_error_result = error

    # 校验错误结果
    def compile_error_result(self, data):
        self.result = data
        if data != self.at_error_result:
            return 1
        return 2

    # 开启正确校验结果
    def on_compile_suc_result(self, suc):
        self.at_result_pattern = re.compile(self.at_name)
        self.at_suc_result = suc

    # 校验正确结果
    def compile_suc_result(self, data):
        self.result = data
        if data == self.at_suc_result:
            return 1
        return 2

    # 关闭校验结果(复位)
    def off_compile_result(self):
        self.at_result_pattern = None
        self.at_error_result = None
        self.at_suc_result = None

    # 获取执行结果
    def get_result(self):
        return self.result
