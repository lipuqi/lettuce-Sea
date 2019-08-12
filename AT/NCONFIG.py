from AT.ATBase import ATBase
"""
AT配置指令
"""


class NCONFIG(ATBase):

    def __init__(self, serialPort, receiveMsg):
        super(NCONFIG, self).__init__(serialPort, receiveMsg)
        self.at_name = "NCONFIG"

