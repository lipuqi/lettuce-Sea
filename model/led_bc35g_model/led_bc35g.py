from common import *
from model.Encoder import Encoder
import sys

# ------------------------------------------------------------------------------
# led 模块
# ------------------------------------------------------------------------------

log = Logger().logger


class main_model:
    def __init__(self, running_manage, drive):
        self.conf = conf_u.read_action(r"model/led_bc35g_model/led_profile.yaml")["Profile"]
        self.model_conf = conf_u.read_action(r"model/led_bc35g_model/led_model_conf.yaml")
        self.rm = running_manage
        self.led = drive["led"].Led(running_manage)
        self.action_switch = {
            "current_led_status": self.current_led_status_properties,
            "current_led_pattern": self.current_led_pattern_properties,
            "switch_led": self.switch_led_command,
            "switch_led_pattern": self.switch_led_pattern_command
        }

    def main(self, action_name, params=None, is_res=True):
        try:
            result = self.action_switch[action_name](params)
            if is_res and result:
                self.rm.send_message.put(result)
        except KeyError:
            log.error("模块没有找到指定的执行方法")
            log.exception(sys.exc_info())

    def switch_led_command(self, params):
        command_name = "switch_led"
        result_param = [params["mid"]]
        try:
            self.led.led_on_off(params["led_status"])
            result_param.append(0)
            result_param.append(0)
        except:
            result_param.append(1)
            result_param.append(1)
            log.error("switch_led_command 执行失败")
            log.exception(sys.exc_info())
        return Encoder(self .conf).packaging_commands(command_name, result_param)

    def switch_led_pattern_command(self, params):
        command_name = "switch_led_pattern"
        result_param = [params["mid"]]
        try:
            if params["led_pattern"] == 0:
                raise RuntimeError('参数非法')
            pattern = self.model_conf["Pattern"][params["led_pattern"]]
            pattern_param = pattern["param"][params["pattern_val"]]
            self.led.led_pattern(params["led_pattern"], pattern_param["frequency"], pattern_param["dc"])
            result_param.append(0)
            result_param.append(0)
        except:
            result_param.append(1)
            result_param.append(1)
            log.error("switch_led_pattern_command 执行失败")
            log.exception(sys.exc_info())
        return Encoder(self.conf).packaging_commands(command_name, result_param)

    def current_led_status_properties(self, params):
        properties_name = "current_led_status"
        result_param = [self.led.get_status()]
        return Encoder(self.conf).packaging_properties(properties_name, result_param)

    def current_led_pattern_properties(self, params):
        properties_name = "current_led_pattern"
        result_param = [self.led.get_pattern()]
        return Encoder(self.conf).packaging_properties(properties_name, result_param)

    def quit_model(self):
        self.led.gpio_quit()
        self.led.gio.cleanup()
