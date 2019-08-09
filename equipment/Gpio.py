import RPi.GPIO as GPIO


class Gpio:
    def __init__(self):
        super(Gpio, self).__init__()
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        self.out_ios = []
        self.in_ios = []

    def setup_out_io(self, out_io):
        if out_io in self.out_ios:
            print("指定输出io口失败，已经被占用")
        else:
            GPIO.setup(out_io, GPIO.OUT, initial=GPIO.LOW)
            self.out_ios.append(out_io)

    def setup_in_io(self, in_io):
        if in_io in self.in_ios:
            print("指定输入io口失败，已经被占用")
        else:
            GPIO.setup(in_io, GPIO.IN)
            self.in_ios.append(in_io)

    def execute_cleanup(self):
        GPIO.cleanup()

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
