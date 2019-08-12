"""
串口数据接收模块
"""

class ReceiveMsg:

    def __init__(self, serialPort, nnmi):
        super(ReceiveMsg, self).__init__()
        self.nnmi = nnmi   # 接收数据模块
        self.serialPort = serialPort  # 串口基础操作模块
        self.atObj = None  # 发送AT指令的模块
        self.quit_sys = 0  # 退出（此参数3个线程同步）
        self.is_pause = 0  # 暂停（此参数3个线程同步）

    #  处理消息的线程方法
    def receive_data(self):
        while self.quit_sys == 0:
            while self.is_pause == 1:
                pass
            result = self.serialPort.read_data()  # 接收数据
            if result:
                # 先匹配是否为上报数据，不是则匹配是否为发送指令的回值
                if self.nnmi.at_result_pattern.search(result):
                    at_result = result.split(":")
                    print("接到数据")
                    print(at_result[1])
                    self.nnmi.add_order(at_result[1])
                elif self.atObj:
                    if self.atObj.compile_result(result):
                        self.atObj = None
                else:
                    print("未设置匹配项数据")
                    print(result)

    #  退出程序标识
    def set_quit_sys(self):
        self.quit_sys = 1

    #  暂停程序标识
    def set_is_pause(self, data):
        self.is_pause = data
