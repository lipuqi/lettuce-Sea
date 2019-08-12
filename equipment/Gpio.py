import RPi.GPIO as GPIO
"""
GPIO设备基础操作模块
"""


class Gpio:
    def __init__(self):
        super(Gpio, self).__init__()
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)  # 使用BCM编号编程
        self.out_ios = []  # 输出编号队列记录
        self.in_ios = []  # 输入编号队列记录

    # 初始化输出端口
    def setup_out_io(self, out_io):
        if out_io in self.out_ios:
            print("指定输出io口失败，已经被占用")
        else:
            GPIO.setup(out_io, GPIO.OUT, initial=GPIO.LOW)
            self.out_ios.append(out_io)

    # 初始化输入端口
    def setup_in_io(self, in_io):
        if in_io in self.in_ios:
            print("指定输入io口失败，已经被占用")
        else:
            GPIO.setup(in_io, GPIO.IN)
            self.in_ios.append(in_io)

    # 清除GPIO口
    def execute_cleanup(self):
        GPIO.cleanup()

    # 执行输出
    def execute_output(self, gpio_id, data):
        try:
            if data == 0:
                GPIO.output(gpio_id, False)
                return 1
            elif data == 1:
                GPIO.output(gpio_id, True)
                return 1
            else:
                print("传入数据有误 -> " + data)
                return 0
        except:
            return 0
