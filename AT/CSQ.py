from AT.ATBase import ATBase
"""
AT信号指令
"""


class CSQ(ATBase):

    def __init__(self, serialPort, receiveMsg):
        super(CSQ, self).__init__(serialPort, receiveMsg)
        self.at_name = "CSQ"

    def execute_at(self):
        super().on_compile_error_result("99,99")
        return super().execute_at()

