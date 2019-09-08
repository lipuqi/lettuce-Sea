from common import *
import sys

log = Logger().logger


def _joint_param(params, data):
    result = ""
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


class Encoder:
    def __init__(self, protocol_id, data=None):
        self.conf = conf_u.read_action(r"upgrade\PCP_protocol.yaml")["Protocol"]
        self.p_id = protocol_id
        self.data = data

    def packaging(self):
        result = ""
        try:
            structure_conf = self.conf["structure"]
            head = byte_u.int2byte(structure_conf["head"]["default_data"], structure_conf["head"]["data_length"] * 2)
            pcp_version = byte_u.int2byte(structure_conf["pcp_version"]["default_data"],
                                          structure_conf["pcp_version"]["data_length"] * 2)
            msg_code = byte_u.int2byte(int(self.p_id), structure_conf["msg_code"]["data_length"] * 2)
            check_code = byte_u.int2byte(structure_conf["check_code"]["default_data"],
                                         structure_conf["check_code"]["data_length"] * 2)
            data_len = byte_u.int2byte(structure_conf["data_len"]["default_data"],
                                       structure_conf["data_len"]["data_length"] * 2)
            data = ""
            if self.data:
                data = _joint_param(structure_conf["data"][self.p_id]["res"], self.data)
                data_len = byte_u.int2byte(len(data) // 2, structure_conf["data_len"]["data_length"] * 2)
            result = head + pcp_version + msg_code + check_code + data_len + data
            check_code = crc_u.crc16_check(result)
            result = head + pcp_version + msg_code + check_code + data_len + data
        except KeyError:
            log.error("打包失败，请核对配置文件中是否有该参数")
            log.exception(sys.exc_info())
            return None
        return result.upper()
