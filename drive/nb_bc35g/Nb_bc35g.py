import serial
from common import *
from drive.Basic_connect_drive import Basic_connect_drive
import drive.nb_bc35g as nb_model
import drive.nb_bc35g.AT_order as AT_order
import time


# ------------------------------------------------------------------------------
# Nb模块 bc-35g设备驱动
# ------------------------------------------------------------------------------

log = Logger().logger
message = nb_model.decode().result_cla(AT_order.get_msg_order)
inform = nb_model.decode().result_cla(AT_order.get_inform_order)


class connect_drive(Basic_connect_drive):

    def __init__(self, running_manage):
        super(connect_drive, self).__init__(running_manage)
        self._basic_cof = conf_u.read_action(r"drive/nb_bc35g/nb_bc35g_conf.yaml")["Basic_cof"]

        self.port = serial.Serial(self._basic_cof["serial_port"], self._basic_cof["baud_rate"],
                                  timeout=self._basic_cof["time_out"])  # 串口，波特率，超时时间
        # 初始化时先关闭，再开启，确保串口是开启状态
        self.port.close()
        if not self.port.isOpen():
            self.port.open()

        self._sign_order = None

    # 开启串口
    def port_open(self):
        if not self.port.isOpen():
            log.info("开启串口")
            self.port.open()

    # 关闭串口
    def port_close(self):
        log.info("关闭串口")
        self.port.flushOutput()
        self.port.close()
        self.port = None

    # 读取串口数据
    def read_data(self):
        result = self.port.readline().decode('utf-8').strip()
        if result:
            log.info("数据进入 " + result)
            if self._sign_order.is_hit(result):
                pass
            elif message.is_hit(result):
                res = message.get_order_result()
                r = res.split(",")
                if r[1][:4] == "FFFE":
                    self.rm.upgrade.put(res)
                else:
                    self.rm.new_message.put(res)
            elif inform.is_hit(result):
                res = inform.get_order_result()
                self.rm.inform.put(res)

    # 将AT指令拼接后发送至串口
    def write_data(self, order_name, order_identify=None, data=None, retry=1, order_result=None, is_verify=True,
                   error_result=None,
                   suc_result=None, delay=1):
        at = nb_model.encoder(order_name, order_identify=order_identify, data=data, retry=retry)
        if is_verify:
            if error_result or suc_result:
                self._sign_order = nb_model.decode().result_cla(order_name, order_result, error_result, suc_result)
            else:
                self._sign_order = nb_model.decode().command_cla(order_name, order_result)
        else:
            self._sign_order = nb_model.decode().result_cla(order_name, order_result)
        at_write = at.get_at_order()
        while at.is_retry():
            time.sleep(delay)
            log.info("执行指令 " + at_write)
            n = self.port.write(at_write.encode())
            if n != 0:
                if is_verify:
                    if self._sign_order.get_order_status():
                        return True
                else:
                    if self._sign_order.get_order_result():
                        return self._sign_order.get_order_result()
                at.flow()

        return False

    # 重启指令
    def restart_at(self):
        self.rm.read_data_thread_pause = True
        at = nb_model.encoder(nb_model.AT_order.restart_order)
        n = self.port.write(at.get_at_order().encode())
        self.port_close()
        time.sleep(3)
        self.port_open()
        self._sign_order = nb_model.decode().command_cla(nb_model.AT_order.restart_order)
        time.sleep(3)
        self.rm.read_data_thread_pause = False
        time.sleep(1)
        if n != 0:
            return self._sign_order.get_order_status()

    # 发送指令 AT+CSQ
    def send_at(self, order_name, retry=1, order_result=None, is_verify=True, error_result=None,
                suc_result=None, delay=1):
        return self.write_data(order_name, retry=retry, order_result=order_result, is_verify=is_verify,
                               error_result=error_result,
                               suc_result=suc_result, delay=delay)

    # 查询指令 AT+CGATT?
    def query_at(self, order_name, retry=1, order_result=None, is_verify=True, error_result=None,
                 suc_result=None, delay=1):
        return self.write_data(order_name, order_identify=nb_model.encoder.query, retry=retry, order_result=order_result,
                               is_verify=is_verify, error_result=error_result,
                               suc_result=suc_result, delay=delay)

    # 执行指令 AT+NMGS=
    def execute_at(self, order_name, *data, retry=1, order_result=None, is_verify=True, error_result=None,
                   suc_result=None, delay=1):
        return self.write_data(order_name, order_identify=nb_model.encoder.execute, data=data, retry=retry,
                               order_result=order_result,
                               is_verify=is_verify, error_result=error_result,
                               suc_result=suc_result, delay=delay)

    # 发送消息
    def send_msg(self, data):
        data = str(len(data) // 2) + "," + data
        return self.execute_at(nb_model.AT_order.send_msg_order, data, retry=3, delay=3)

    # 模组初始化
    def init(self, conf_file=None):
        time.sleep(1)
        log.info("开始初始化")
        init_conf = conf_u.read_action(r"drive/nb_bc35g/init_yml/default_init_conf.yaml")["Nb_init"]
        if conf_file:
            init_conf = conf_u.read_action(conf_file)["Nb_init"]
        if not self.query_at(nb_model.AT_order.CDP_server_order, suc_result=init_conf["CDP_server"]):
            if not self.setup_cdp(init_conf["CDP_server"]):
                return False
        if not self.query_at(nb_model.AT_order.band_order, suc_result=init_conf["band_val"]):
            if not self.execute_at(nb_model.AT_order.band_order, init_conf["band_val"]):
                return False
        if init_conf["eDRX"] == 0:
            if not self.execute_at(nb_model.AT_order.eDRX_order, "0,5"):
                return False
        if init_conf["PSM"] == 0:
            if not self.execute_at(nb_model.AT_order.PSM_order, "0"):
                return False
        if not self.network():
            return False
        log.info("初始化成功")
        return True

    # 模组入网失败重试
    def network_error(self):
        if not self.restart_at():
            return False
        if not self.execute_at(nb_model.AT_order.RF_order, "0"):
            return False
        if not self.send_at(nb_model.AT_order.clean_RF_order):
            return False
        return True

    # 模组入网
    def network(self, retry_network=3):
        if not self.execute_at(nb_model.AT_order.RF_order, "1"):
            return False
        if not self.execute_at(nb_model.AT_order.network_order, "1", delay=3, retry=3):
            return False
        if not self.query_at(nb_model.AT_order.network_order, retry=3, delay=5, suc_result="1"):
            while retry_network != 0:
                retry_network -= 1
                if self.network_error():
                    if self.network(retry_network=retry_network):
                        return True
            return False
        return True

    # 进入IDLE模式
    def access_idle(self):
        if not self.execute_at(nb_model.AT_order.send_inform_order, "3,AA34BB,0x0001"):
            return False
        return True

    # 退出
    def break_connect(self):
        self.access_idle()
        self.execute_at(nb_model.AT_order.RF_order, "0")
        self.rm.read_data_thread_quit = True
        time.sleep(3)
        self.port_close()

    # 模组健康检测
    def health_monitoring(self):
        if not self.send_at(nb_model.AT_order.signal_order, retry=3, error_result="99,99", delay=5):
            if not self.network_again():
                return False
        return True

    # 模组重新入网
    def network_again(self):
        if self.network_error():
            if self.network():
                return True
        return False

    # 模组设置平台IP
    def setup_cdp(self, server_addr):
        if not self.execute_at(nb_model.AT_order.network_conf_order, "AUTOCONNECT,FALSE"):
            return False
        if not self.execute_at(nb_model.AT_order.CDP_server_order, server_addr):
            return False
        if self.restart_at():
            return True
        return False
