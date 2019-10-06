import RPi.GPIO as Gpio

# ------------------------------------------------------------------------------
# 基础设备类
# ------------------------------------------------------------------------------


class Basic_drive:
    pin_values = [Gpio.LOW, Gpio.HIGH]
    pull_resistors = [Gpio.PUD_DOWN, Gpio.PUD_UP]

    def __init__(self, rm, pin_in_id=[], pin_out_id=[]):
        self.pin_in_id = pin_in_id
        self.pin_out_id = pin_out_id
        self.gio = Gpio
        self.running_manage = rm

        self._pwm = {}

    # 初始化接口
    def _gpio_init(self):
        self.gio.setwarnings(False)
        self.gio.setmode(Gpio.BCM)

        if self.pin_in_id:
            for pin_io in self.pin_in_id:
                for io_name in list(pin_io.keys()):
                    pin_id = pin_io[io_name]["pin_id"]
                    default = pin_io[io_name]["default"]
                    if self.running_manage.setup_in_io(pin_id):
                        self.gio.setup(pin_id, Gpio.IN, pull_up_down=self.pull_resistors[default])

        if self.pin_out_id:
            for pin_io in self.pin_out_id:
                for io_name in list(pin_io.keys()):
                    pin_id = pin_io[io_name]["pin_id"]
                    default = pin_io[io_name]["default"]
                    if self.running_manage.setup_out_io(pin_id):
                        self.gio.setup(pin_id, Gpio.OUT, initial=self.pin_values[default])

    # 脉冲设置
    def _pwm_start(self, pin, frequency, dc):
        if pin in self._pwm:
            if self._pwm[pin]["fre"] != frequency:
                self._pwm[pin]["pwm_obj"].ChangeFrequency(frequency)
            if self._pwm[pin]["dc"] != dc:
                self._pwm[pin]["pwm_obj"].ChangeDutyCycle(dc)

        else:
            self._pwm[pin] = {'fre': frequency, 'dc': dc, "pwm_obj": self.gio.PWM(pin, frequency)}
            self._pwm[pin]["pwm_obj"].start(dc)

    # 脉冲退出
    def _pwm_stop(self, pin):
        if pin in self._pwm:
            self._pwm[pin]["pwm_obj"].stop()
            del self._pwm[pin]

    # 复位
    def drive_reset(self):
        if self.pin_out_id:
            for pin_io in self.pin_out_id:
                for io_name in list(pin_io.keys()):
                    pin_id = pin_io[io_name]["pin_id"]
                    default = pin_io[io_name]["default"]
                    self.gio.output(pin_id, self.pin_values[default])

    # 退出
    def gpio_quit(self):
        self.running_manage.clear_pin(self.pin_in_id + self.pin_out_id)