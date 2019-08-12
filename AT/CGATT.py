from AT.ATBase import ATBase
import time
"""
AT入网指令
"""


class CGATT(ATBase):

    def __init__(self, serialPort, receiveMsg):
        super(CGATT, self).__init__(serialPort, receiveMsg)
        self.at_name = "CGATT"

    # 执行后校对结果
    def integration_at(self, data):
        super().execute_at(data)
        super().on_compile_suc_result(data)
        time.sleep(10)
        return super().query_at()


