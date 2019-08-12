from AT.ATBase import ATBase
import time
"""
AT射频指令
"""


class CFUN(ATBase):

    def __init__(self, serialPort, receiveMsg):
        super(CFUN, self).__init__(serialPort, receiveMsg)
        self.at_name = "CFUN"

    # 执行后校对结果
    def integration_at(self, data):
        super().execute_at(data)
        super().on_compile_suc_result(data)
        time.sleep(5)
        return super().query_at()

