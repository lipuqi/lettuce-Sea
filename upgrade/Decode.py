from common import *
import sys

log = Logger().logger


class Decode:
    def __init__(self, data):
        self.conf = conf_u.read_action(r"upgrade\PCP_protocol.yaml")["Protocol"]
        self.data = data

    # 解析消息
    def parse_msg(self):
        try:
            structure_conf = self.conf["structure"]
            check_code_start = (structure_conf["head"]["data_length"] + structure_conf["pcp_version"]["data_length"] +
                                structure_conf["msg_code"]["data_length"]) * 2
            check_code_end = check_code_start + structure_conf["check_code"]["data_length"] * 2
            check_code = self.data[check_code_start:check_code_end]
            if crc_u.crc16_verify(self.data[:check_code_start] + str(
                    byte_u.int2byte(structure_conf["check_code"]["default_data"],
                                    structure_conf["check_code"]["data_length"] * 2)) + self.data[check_code_end:],
                                  check_code):
                msg_code_start = (structure_conf["head"]["data_length"] + structure_conf["pcp_version"][
                    "data_length"]) * 2
                msg_code_end = msg_code_start + structure_conf["msg_code"]["data_length"] * 2
                msg_code = str(byte_u.byte2int(self.data[msg_code_start:msg_code_end]))

                data_len_start = check_code_end
                data_len_end = data_len_start + structure_conf["data_len"]["data_length"] * 2
                data_len = byte_u.byte2int(self.data[data_len_start:data_len_end])
                command_name = structure_conf["data"][msg_code]["command_name"]

                if data_len != 0:
                    params = {}
                    data = self.data[data_len_end:]
                    for param in structure_conf["data"][msg_code]["req"]:
                        data_name = param["data_name"]
                        if param["data_type"] == 'data':
                            params[data_name] = byte_u.byte2bytes(data)
                        else:
                            index = int(param["data_length"]) * 2
                            param_data = data[:index]
                            data = data[index:]
                            if param["data_type"] == 'string':
                                params[data_name] = byte_u.byte2str(param_data)
                            else:
                                params[data_name] = byte_u.byte2int(param_data)
                    return msg_code, command_name, params
                else:
                    return msg_code, command_name, None
            else:
                return None, None, None
        except KeyError:
            log.error("解析命令失败，请核对配置文件中是否有该命令")
            log.exception(sys.exc_info())
            return None, None, None
