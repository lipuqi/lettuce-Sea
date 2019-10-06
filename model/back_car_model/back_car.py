from common import *
from model.Encoder import Encoder
import threading
import sys

# ------------------------------------------------------------------------------
# 倒车模块
# ------------------------------------------------------------------------------

log = Logger().logger


class main_model:
    def __init__(self, running_manage, drive):
        self.conf = conf_u.read_action(r"model/back_car_model/back_car_profile.yaml")["Profile"]
        self.model_conf = conf_u.read_action(r"model/back_car_model/back_car_conf.yaml")
        self.rm = running_manage
        self._status = 0

        self.led = drive["led"].Led(running_manage)
        self.buzzer = drive["buzzer"].Buzzer(running_manage)
        self.ultrasonic_sensors = drive["ultrasonic_sensors"].Ultrasonic_sensors(running_manage)

        self.action_switch = {
            "current_back_car_status": self.current_back_car_status,
            "switch_back_car": self.switch_back_car
        }

    def main(self, action_name, params=None, is_res=True):
        try:
            result = self.action_switch[action_name](params)
            if is_res and result:
                self.rm.send_message.put(result)
        except KeyError:
            log.error("模块没有找到指定的执行方法")
            log.exception(sys.exc_info())

    def current_back_car_status(self, params):
        properties_name = "current_back_car_status"
        result_param = [self._status]
        return Encoder(self.conf).packaging_properties(properties_name, result_param)

    def switch_back_car(self, params):
        command_name = "switch_back_car"
        result_param = [params["mid"]]
        try:
            if params["back_car_status"] == 0:
                self._status = 0
                self.back_car_off()
            else:
                self._status = 1
                threading.Thread(target=self.back_car_on).start()
            result_param.append(0)
            result_param.append(0)
        except:
            result_param.append(1)
            result_param.append(1)
            log.error("switch_led_command 执行失败")
            log.exception(sys.exc_info())
        return Encoder(self.conf).packaging_commands(command_name, result_param)

    def back_car_on(self):
        pattern = self.model_conf["Pattern"]
        alarm_level = self.model_conf["model_conf"]["alarm"]
        next_result_mm = 0
        while self._status == 1:
            result_mm = self.ultrasonic_sensors.get_real_data()
            if result_mm < 0 or result_mm > 2000:
                continue
            if next_result_mm != result_mm:
                next_result_mm = result_mm
            else:
                continue
            for level_key in list(alarm_level.keys()):
                level = alarm_level[level_key]
                if level["max_val"] > result_mm > level["min_val"]:
                    led = level["led"]
                    buzzer = level["buzzer"]
                    if led["pattern"] == -1:
                        self.led.led_on_off(led["val"])
                    else:
                        led_pattern_param = pattern["led"]["param"][led["val"]]
                        self.led.led_pattern(led["val"], led_pattern_param["frequency"], led_pattern_param["dc"])
                    if buzzer["pattern"] == -1:
                        self.buzzer.buzzer_on_off(buzzer["val"])
                    else:
                        buzzer_pattern_param = pattern["buzzer"]["param"][buzzer["val"]]
                        self.buzzer.buzzer_pattern(buzzer["val"], buzzer_pattern_param["frequency"],
                                             buzzer_pattern_param["dc"])
                    break


    def back_car_off(self):
        self.ultrasonic_sensors.drive_reset()
        self.led.drive_reset()
        self.buzzer.drive_reset()

    def quit_model(self):
        self._status = 0
        self.ultrasonic_sensors.gpio_quit()
        self.led.gpio_quit()
        self.buzzer.gpio_quit()
        self.led.gio.cleanup()

