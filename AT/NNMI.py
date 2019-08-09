import re


class NNMI:

    def __init__(self):
        super(NNMI, self).__init__()
        self.at_name = "NNMI"
        self.at_result_pattern = re.compile(self.at_name)
        self.wait_list = []

    def add_order(self, order):
        if order in self.wait_list:
            return
        else:
            self.wait_list.append(order)

    def del_order(self, order):
        while order in self.wait_list:
            self.wait_list.remove(order)


