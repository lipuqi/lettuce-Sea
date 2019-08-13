import re
"""
接收平台状态
"""


class QLWEVTIND:

    def __init__(self):
        self.at_name = "QLWEVTIND"
        self.at_result_pattern = re.compile(self.at_name)

    #  解析平台消息
    def oc_analysis_msg(self, data):
        if data == "3":
            print("成功连接到华为OceanConnect平台")


