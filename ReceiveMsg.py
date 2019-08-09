import re


class ReceiveMsg:

    def __init__(self, serialPort, nnmi):
        super(ReceiveMsg, self).__init__()
        self.nnmi = nnmi
        self.serialPort = serialPort
        self.error = re.compile('ERROR')
        self.ok = re.compile('OK')
        self.atObj = None
        self.quit_sys = 0
        self.is_pause = 0

    def receive_data(self):
        while self.quit_sys == 0:
            while self.is_pause == 1:
                pass
            result = self.serialPort.read_data()
            if result:
                if self.atObj:
                    if self.atObj.at_result_pattern:
                        if self.atObj.at_result_pattern.search(result):
                            at_result = result.split(":")
                            if self.atObj.at_error_result and at_result[1] == self.atObj.at_error_result:
                                self.atObj.update_status(2)
                                self.atObj = None
                                print(result)
                            elif self.atObj.at_suc_result and at_result[1] == self.atObj.at_suc_result:
                                self.atObj.update_status(1)
                                self.atObj = None
                                print(result)
                            else:
                                print("正则没有匹配项\n")
                                self.atObj.update_status(1)
                                self.atObj = None
                                print(result)
                        else:
                            print("正则没有匹配项\n")
                            self.atObj.update_status(1)
                            self.atObj = None
                            print(result)
                    else:
                        if self.ok.search(result):
                            self.atObj.update_status(1)
                            self.atObj = None
                            print(result)
                        elif self.error.search(result):
                            self.atObj.update_status(2)
                            self.atObj = None
                            print(result)
                if self.nnmi.at_result_pattern.search(result):
                    at_result = result.split(":")
                    print("接到数据")
                    print(at_result[1])
                    self.nnmi.add_order(at_result[1])

    def set_quit_sys(self):
        self.quit_sys = 1

    def set_is_pause(self, data):
        self.is_pause = data
