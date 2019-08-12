import serial

"""
串口基础操作模块
"""


class SerialPort:

    def __init__(self, port, buand):
        super(SerialPort, self).__init__()
        self.port = serial.Serial(port, buand, timeout=0.5)  # 串口，波特率，超时时间
        # 初始化时先关闭，再开启，确保串口是开启状态
        self.port.close()
        if not self.port.isOpen():
            self.port.open()

    # 开启串口
    def port_open(self):
        if not self.port.isOpen():
            self.port.open()

    # 关闭串口
    def port_close(self):
        self.port.flushOutput()
        self.port.close()

    # 读取串口数据
    def read_data(self):
        return self.port.readline().decode('utf-8').strip()

    # 将AT指令拼接后发送至串口
    def write_data(self, at_name, at_symbol, data):
        at = 'AT+' + at_name
        # 如果标识不为空则拼接参数
        if at_symbol:
            at += at_symbol
            if data:
                at += data
        at += '\n'
        print(at)
        n = self.port.write(at.encode())
        return n
