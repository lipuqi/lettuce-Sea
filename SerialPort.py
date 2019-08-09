import serial


class SerialPort:

    def __init__(self, port, buand):
        super(SerialPort, self).__init__()
        self.port = serial.Serial(port, buand, timeout=0.5)
        self.port.close()
        if not self.port.isOpen():
            self.port.open()

    def port_open(self):
        if not self.port.isOpen():
            self.port.open()

    def port_close(self):
        self.port.flushOutput()
        self.port.close()

    def read_data(self):
        return self.port.readline().decode('utf-8').strip()

    def write_data(self, at_name, at_symbol, data):
        at = 'AT+' + at_name
        if at_symbol:
            at += at_symbol
        if data:
            at += data
        at += '\n'
        print(at)
        n = self.port.write(at.encode())
        return n
