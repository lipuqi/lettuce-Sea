from drive.Basic_drive import Basic_drive
import common.Conf_utils as Cu
from common.Log_utils import Logger
import common.Time_utils as time_u


log = Logger().logger


class Ultrasonic_sensors(Basic_drive):

    def __init__(self, rm):
        self._pin_id = Cu.read_action(r"drive/ultrasonic_sensors/ultrasonic_sensors_conf.yaml")["Pin"]
        super(Ultrasonic_sensors, self).__init__(rm, pin_out_id=self._pin_id["out_io"], pin_in_id=self._pin_id["in_io"])

        self._status = 0  # 状态0不工作，1工作状态
        self._main_io_out = self.pin_out_id[0]["ultrasonic_sensors_out"]["pin_id"]  # 主要IO口
        self._main_io_in = self.pin_in_id[0]["ultrasonic_sensors_in"]["pin_id"]  # 主要IO口

        self._gpio_init()

    # 触发一次检测超声波距离（mm)
    def get_real_data(self):
        time_utils = time_u.Time_utils()
        time_u.delay_ms(100)
        self.gio.output(self._main_io_out, self.pin_values[1])
        time_u.delay_us(10)
        self.gio.output(self._main_io_out, self.pin_values[0])
        while self.gio.input(self._main_io_in) == self.pin_values[0]:
            pass
        time_utils.set_time_date(time_u.get_now_time())
        while self.gio.input(self._main_io_in) == self.pin_values[1]:
            pass
        result_us = time_utils.diff_time_us(time_u.get_now_time())
        return result_us * 340 / 2

    def get_status(self):
        return self._status

    def drive_reset(self):
        super().drive_reset()
        self._status = 0

    def gpio_quit(self):
        self.drive_reset()
        super().gpio_quit()
