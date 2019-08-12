from AT.ATBase import ATBase
"""
AT RAI指令
"""


class QLWULDATAEX(ATBase):

    def __init__(self, serialPort, receiveMsg):
        super(QLWULDATAEX, self).__init__(serialPort, receiveMsg)
        self.at_name = "QLWULDATAEX"


