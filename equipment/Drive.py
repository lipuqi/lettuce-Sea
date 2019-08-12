import time
"""
硬件调度中心
"""


class Drive:

    def __init__(self, nnmi, receiveMsg, led, pi):
        super(Drive, self).__init__()
        self.nnmi = nnmi  # 接收数据模块
        self.receiveMsg = receiveMsg  # 串口数据接收模块
        self.led = led  # 灯
        self.pi = pi  # 树莓派

    # 循环处查询列表内任务线程方法
    def order_monitor(self):
        while self.receiveMsg.quit_sys == 0:
            time.sleep(2)
            while self.receiveMsg.is_pause == 1:
                pass
            if self.nnmi.wait_list:
                for order in self.nnmi.wait_list:
                    self.nnmi.del_order(order)
                    self.analysis_msg(order)

    # 处理任务调度硬件模块
    def analysis_msg(self, data):
        # 分割接收消息
        msg_result = data.split(",")
        msg_len = msg_result[0]
        msg_data = msg_result[1]
        if msg_len == "4":
            message_id = int(msg_data[:2])
            mid = msg_data[2:6]
            value = int(msg_data[6:])
            if message_id == 1:
                self.led.set_mid(mid)
                self.led.led_on_off(value)
            elif message_id == 3:
                self.led.set_mid(mid)
                self.led.query_status()
            elif message_id == 6:
                self.pi.set_mid(mid)
                self.pi.execute_quit()
            else:
                print("无解析类型")
        else:
            print("命令下发长度不符合")
