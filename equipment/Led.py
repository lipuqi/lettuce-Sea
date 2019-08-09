
class Led:
    def __init__(self, ioObj, nmgs):
        super(Led, self).__init__()
        self.status = 0
        self.ioObj = ioObj
        self.nmgs = nmgs
        self.io_id = 4
        self.ioObj.setup_out_io(self.io_id)
        self.mid = None

    def led_on_off(self, data):
        suc = "02" + self.mid + "00" + '%02x' % data
        fail = "02" + self.mid + "01" + '%02x' % data
        if data != 0 and data != 1:
            print("开关灯只接受0/1")
            self.nmgs.execute_at(fail)
        else:
            if data == self.status:
                self.nmgs.execute_at(suc)
            else:
                execute_result = self.ioObj.execute_output(self.io_id, data)
                if execute_result == 1:
                    self.status = data
                    self.nmgs.execute_at(suc)
                else:
                    self.nmgs.execute_at(fail)

    def query_status(self):
        suc = "04" + self.mid + "00" + '%02x' % self.status
        self.nmgs.execute_at(suc)

    def led_status(self):
        return self.status

    def set_mid(self, mid):
        self.mid = mid