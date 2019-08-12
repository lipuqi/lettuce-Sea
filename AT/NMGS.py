from AT.ATBase import ATBase
"""
AT 发送信息指令
"""


class NMGS(ATBase):

    def __init__(self, serialPort, receiveMsg):
        super(NMGS, self).__init__(serialPort, receiveMsg)
        self.at_name = "NMGS"

    def execute_at(self, data):
        new_data = str(int(len(data) / 2)) + "," + data  # 拼接数据的长度部分
        return super().execute_at(new_data)


