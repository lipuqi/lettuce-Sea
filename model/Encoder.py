from common import *
import sys

# ------------------------------------------------------------------------------
# 模块消息解析
# ------------------------------------------------------------------------------

log = Logger().logger


def _joint_param(result, params, data):
    paras_len = len(params)
    if paras_len != len(data):
        log.error("入参列表参数个数与配置表不符")
        return None
    for i in range(0, paras_len):
        p = params[i]
        data_length = int(p["data_length"]) * 2
        if data[i]:
            if p["data_type"] == "string":
                result += byte_u.str2byte(data[i], data_length)
            else:
                result += byte_u.int2byte(data[i], data_length)
        else:
            result += byte_u.int2byte(p["default_data"], data_length)
    return result


def _get_com_id(commands, com_name):
    for com_id in commands:
        if commands[com_id]["command_name"] == com_name:
            return com_id
    return None


class Encoder:
    def __init__(self, conf):
        self.conf = conf

    # 打包上传属性
    def packaging_properties(self, pro_name, data):
        result = ""
        try:
            pro = self.conf["properties"][pro_name]
            result += pro["message_id"]
            paras = pro["paras"]
            result = _joint_param(result, paras, data)
        except KeyError:
            log.error("打包失败，请核对配置文件中是否有该参数")
            log.exception(sys.exc_info())
            return None
        return result

    # 打包回复指令
    def packaging_commands(self, com_name, data):
        result = ""
        try:
            com_id = _get_com_id(self.conf["commands"], com_name)
            if not com_id:
                raise KeyError
            com_data = self.conf["commands"][com_id]
            if "res" not in com_data:
                return None
            result += byte_u.plus(com_id, 1)
            result = _joint_param(result, com_data["res"], data)
        except KeyError:
            log.error("打包失败，请核对配置文件中是否有该参数")
            log.exception(sys.exc_info())
            return None
        return result


