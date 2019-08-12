from AT.ATBase import ATBase
import time

"""
AT重启指令
"""


class NRB(ATBase):

    def __init__(self, serialPort, receiveMsg):
        super(NRB, self).__init__(serialPort, receiveMsg)
        self.at_name = "NRB"

    #  执行重启
    def execute_at(self):
        print("执行重启")
        super().receiveMsg.set_is_pause(1)  # 全体线程置为暂停位
        super().serialPort.write_data(self.at_name, None, None)
        super().serialPort.port_close()  # 关闭串口
        time.sleep(3)
        super().serialPort.port_open()  # 开启串口
        super().receiveMsg.atObj = self
        super().status = 0
        time.sleep(3)
        super().receiveMsg.set_is_pause(0)  # 全体线程置为正常
        time.sleep(1)
        while True:
            if super().retry == 4:
                print("执行失败，不再重试")
                super().retry = 1
                return 2
            if super().status == 1:
                print("执行成功")
                super().retry = 1
                time.sleep(3)
                return 1
            elif super().status == 2:
                print("执行失败，重试" + str(super().retry))
                super().retry += 1
                time.sleep(2)
                return super().execute_at()
