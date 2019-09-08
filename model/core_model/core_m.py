from common import *
from model.Encoder import Encoder
from queue import Queue
import sys

# ------------------------------------------------------------------------------
# 核心模块
# ------------------------------------------------------------------------------

log = Logger().logger


class core_m:
    def __init__(self, running_manage, model_manage):
        self.conf = conf_u.read_action(r"model\core_model\core_profile.yaml")["Profile"]
        self.rm = running_manage
        self.mm = model_manage
        self.task = Queue()
        self.current_task = {}
        self.action_switch = {
            "current_model_id": self.current_model_id_properties,
            "switch_model": self.switch_model_command
        }

    def main(self, action_name, params=None, is_res=True):
        try:
            result = self.action_switch[action_name](params)
            if is_res and result:
                self.rm.send_message.put(result)
        except KeyError:
            log.error("模块没有找到指定的执行方法")
            log.exception(sys.exc_info())

    def current_model_id_properties(self, params):
        properties_name = "current_model_id"
        result_param = [self.mm.current_model_id]
        return Encoder(self.conf).packaging_properties(properties_name, result_param)

    def switch_model_command(self, params):
        command_name = "switch_model"
        result_param = [params["mid"]]
        try:
            result_param.append(0)
            result_param.append(0)
        except:
            result_param.append(1)
            result_param.append(1)
            log.error("switch_model_command 执行失败")
            log.exception(sys.exc_info())
        return Encoder(self .conf).packaging_commands(command_name, result_param)

    def quit_model(self):
        pass




