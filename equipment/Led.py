"""
灯
"""


class Led:
    def __init__(self, ioObj, nmgs):
        super(Led, self).__init__()
        self.status = 0  # 当前灯的状态
        self.ioObj = ioObj  # GPIO设备基础操作模块
        self.nmgs = nmgs  # 发送消息模块
        self.io_id = 4  # 当前设备使用的针脚编号
        self.ioObj.setup_out_io(self.io_id)  # 初始化IO口
        self.mid = None  # 命令下发的响应码

    # 处理灯的开关命令
    def led_on_off(self, data):
        suc = "02" + self.mid + "00" + '%02x' % data  # 成功的返回信息
        fail = "02" + self.mid + "01" + '%02x' % data  # 失败的返回信息
        if data != 0 and data != 1:
            print("开关灯只接受0/1")
            self.nmgs.execute_at(fail)
        else:
            # 如果命令下发状态与当前灯状态一致则直接发送成功
            if data == self.status:
                self.nmgs.execute_at(suc)
            else:
                execute_result = self.ioObj.execute_output(self.io_id, data)
                # 如果执行成功就响应成功
                if execute_result == 1:
                    self.status = data
                    self.nmgs.execute_at(suc)
                else:
                    self.nmgs.execute_at(fail)

    # 处理查询灯当前状态的命令
    def query_status(self):
        suc = "04" + self.mid + "00" + '%02x' % self.status
        self.nmgs.execute_at(suc)

    # 获取灯当前的状态
    def led_status(self):
        return self.status

    # 保存响应码
    def set_mid(self, mid):
        self.mid = mid