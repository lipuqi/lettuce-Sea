import re
"""
接收标识
"""


class NNMI:

    def __init__(self):
        self.at_name = "NNMI"
        self.at_result_pattern = re.compile(self.at_name)
        self.wait_list = []  # 待处理信息列表

    # 添加待处理信息到列表
    def add_order(self, order):
        if order in self.wait_list:
            return
        else:
            self.wait_list.append(order)

    # 从列表删除待处理信息
    def del_order(self, order):
        while order in self.wait_list:
            self.wait_list.remove(order)


