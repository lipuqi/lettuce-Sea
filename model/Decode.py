from common import *
import sys

# ------------------------------------------------------------------------------
# 模块消息解析
# ------------------------------------------------------------------------------


log = Logger().logger


class Decode:
    def __init__(self, data, core_conf, current_model_conf):
        self.data = data
        self.core_conf = core_conf
        self.current_model_conf = current_model_conf

    # 解析数据
    def parse_data(self):
        if self.data[:1] == "0":
            conf = self.core_conf
            model = 0
        else:
            conf = self.current_model_conf
            model = 1

        try:
            command = conf["commands"][self.data[:2]]
            command_name = command["command_name"]
            data = self.data[2:]
            params = {}
            for param in command["req"]:
                data_name = param["data_name"]
                index = int(param["data_length"]) * 2
                param_data = data[:index]
                data = data[index:]
                if param["data_type"] == 'string':
                    params[data_name] = byte_u.byte2str(param_data)
                else:
                    params[data_name] = byte_u.byte2int(param_data)
        except KeyError:
            log.error("解析命令失败，请核对配置文件中是否有该命令")
            log.exception(sys.exc_info())
            return None, None, None
        return model, command_name, params


