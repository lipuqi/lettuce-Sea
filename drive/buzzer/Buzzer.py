from drive.Basic_drive import Basic_drive
import common.Conf_utils as Cu
from common.Log_utils import Logger

# ------------------------------------------------------------------------------
# 蜂鸣器设备驱动（v01）
# ------------------------------------------------------------------------------

log = Logger().logger


class Buzzer(Basic_drive):
    def __init__(self, rm):
        self._pin_id = Cu.read_action(r"drive/buzzer/buzzer_conf.yaml")["Pin"]
        super(Buzzer, self).__init__(rm, pin_out_id=self._pin_id["out_io"])

        self._status = self.pin_out_id[0]["buzzer_out"]["default"]  # 状态0不工作，1工作状态
        self._main_io = self.pin_out_id[0]["buzzer_out"]["pin_id"]  # 主要IO口
        self._pattern = 0  # 模式

        self._gpio_init()

    # 模式设置
    def buzzer_pattern(self, pattern, frequency, dc):
        self._pwm_start(self._main_io, frequency, dc)
        if pattern == 0:
            self._status = 0
        else:
            self._status = 1
        self._pattern = pattern
        log.info("蜂鸣器设置的模式ID为 " + str(pattern))

    # 开关设置
    def buzzer_on_off(self, par):
        if self._pattern == 0 and self._status == par:
            pass
        else:
            super()._pwm_stop(self._main_io)
            self.gio.output(self._main_io, self.pin_values[par])
            self._status = par
            self._pattern = 0
        log.info("蜂鸣器设置为开关模式")

    def get_status(self):
        return self._status

    def get_pattern(self):
        return self._pattern

    # 复位
    def drive_reset(self):
        super()._pwm_stop(self._main_io)
        super().drive_reset()
        self._status = 0
        self._pattern = None

    def gpio_quit(self):
        self.drive_reset()
        super().gpio_quit()
