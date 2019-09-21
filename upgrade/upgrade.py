from common import *
from upgrade.Encoder import Encoder
from upgrade.Decode import Decode
from drive.upgrade_drive import upgrade_drive
from model.upgrade_model import upgrade_model
import sys
import time

log = Logger().logger


class upgrade:
    def __init__(self, running_manage):
        self.machine_code = conf_u.read_action(r"conf/resource/basic_conf.yaml")["Basic_info"]["machine_code"]
        self.current_version = ""
        self.new_version = None
        self.upgrade_status = 0  # 升级状态0就绪，1下载中，2安装中

        self.rm = running_manage
        self.action_switch = {
            "query_device_version": self.query_device_version,
            "new_version_inform": self.new_version_inform,
            "download_new_version": self.download_new_version,
            "download_new_version_status": self.download_new_version_status,
            "execute_upgrade": self.execute_upgrade,
            "upgrade_status": self.upgrade_status_com,
        }

        self.init()

    def init(self):
        self.current_version = conf_u.read_action(r"conf/resource/current_version.yaml")["current_version"]

    def main(self, action_name, msg_code, params=None):
        try:
            self.action_switch[action_name](msg_code, params)
        except KeyError:
            log.error("模块没有找到指定的执行方法")
            log.exception(sys.exc_info())

    def query_device_version(self, msg_code, params):
        if self.new_version:
            return
        param = [0, self.current_version]
        result = Encoder(msg_code, param).packaging()
        self.rm.send_message.put(result)

    def new_version_inform(self, msg_code, params):
        new_version = {}
        param = [0]
        try:
            new_version["new_version"] = params["new_version"]
            new_version["upgrade_single_len"] = params["upgrade_single_len"]
            new_version["upgrade_single_num"] = params["upgrade_single_num"]
            new_version["current_upgrade_single_num"] = 0
            new_version["upgrade_data"] = bytes()
            self.new_version = new_version
            result = Encoder(msg_code, param).packaging()
            self.rm.send_message.put(result)

            time.sleep(5)
            self.download_new_version("21", None)
        except:
            log.error("解析参数失败")
            log.exception(sys.exc_info())
            param = [127]
            result = Encoder(msg_code, param).packaging()
            self.rm.send_message.put(result)

    def download_new_version(self, msg_code, params):
        current_upgrade_index = self.new_version["current_upgrade_single_num"]
        if params:
            if params["res_code"] == 0:
                self.new_version["upgrade_data"] += params["upgrade_single_data"]
            else:
                log.error("请求升级包失败 ：" + str(params["res_code"]))

        if current_upgrade_index < self.new_version["upgrade_single_num"]:
            self.upgrade_status = 1
            param = [self.new_version["new_version"], current_upgrade_index]
            result = Encoder(msg_code, param).packaging()
            self.rm.send_message.put(result)
            self.new_version["current_upgrade_single_num"] = current_upgrade_index + 1
        else:
            self.download_new_version_status("22", 0)

    def download_new_version_status(self, msg_code, params):
        if isinstance(params, dict):
            if params["res_code"] != 0:
                log.error("上报升级包下载状态失败 ：" + str(params["res_code"]))
        else:
            param = [params]
            result = Encoder(msg_code, param).packaging()
            self.rm.send_message.put(result)

    def execute_upgrade(self, msg_code, params):
        param = [0]
        result = Encoder(msg_code, param).packaging()
        self.rm.send_message.put(result)
        time.sleep(5)
        try:
            zip_path = conf_u.get_project_path() + "upgrade/version/" + self.new_version[
                "new_version"] + "/" + "UpgradePackage.zip"
            file_u.write_file(self.new_version["upgrade_data"], zip_path)

            res_path = conf_u.get_project_path() + "upgrade/version/" + self.new_version[
                "new_version"] + "/UpgradePackage"
            file_u.zip_file(zip_path, res_path)

            conf = conf_u.read_action("upgrade/version/" + self.new_version[
                "new_version"] + "/UpgradePackage/UpgradePackageInfo.yaml")
            if self._verify_version(conf["package_info"]):
                self.upgrade_status = 2
                self.rm.execute_running_marking = 1
                index = 60
                while self.rm.running_status != 3:
                    if index < 0:
                        log.error("退出失败")
                        return
                    time.sleep(5)
                    index -= 5
                if self._upgrade(conf["package_info"]["upgrade_type"], res_path, conf["install"]):
                    self.rm.execute_running_marking = 0
                    index = 60
                    while self.rm.running_status != 0:
                        if index < 0:
                            log.error("启动失败")
                            return
                        time.sleep(5)
                        index -= 5
                    self.upgrade_status_com("24", 0)
                    file_u.del_dir_file(res_path)
                else:
                    self.upgrade_status_com("24", 10)
                    log.error("安装失败")
        except:
            log.error("执行升级出现问题")
            log.exception(sys.exc_info())
            self.upgrade_status_com("24", 127)

    def upgrade_status_com(self, msg_code, params):
        if isinstance(params, dict):
            if params["res_code"] != 0:
                log.error("上报升级结果失败 ：" + str(params["res_code"]))
        else:
            param = [params, self.new_version["new_version"]]
            result = Encoder(msg_code, param).packaging()
            self.rm.send_message.put(result)
            if params == 0:
                self._write_conf(self.current_version, self.new_version["new_version"])
                self.current_version = self.new_version["new_version"]
                self.new_version = None
                self.upgrade_status = 0

    def _verify_version(self, conf):
        if conf["upgrade_pattern"] == 0:
            return True
        elif conf["upgrade_pattern"] == 1:
            if self.machine_code in conf["upgrade_list"]:
                return True
            else:
                return False

    def _upgrade(self, upgrade_type, upgrade_path, install_list):
        if upgrade_type == "model":
            return upgrade_model(upgrade_path, install_list).execute_upgrade()
        elif upgrade_type == "drive":
            return upgrade_drive(upgrade_path, install_list).execute_upgrade()
        else:
            log.error("执行升级出现问题")
            return False

    def listener_upgrade(self):
        while not self.rm.upgrade_quit:
            while self.rm.upgrade_pause:
                pass
            if not self.rm.upgrade.empty():
                upgrade = self.rm.upgrade.get()
                u = upgrade.split(",")
                msg_code, command_name, params = Decode(u[1]).parse_msg()
                self.main(command_name, msg_code, params)

    def _write_conf(self, old_version, new_version):
        old_conf = conf_u.read_action(r"conf/resource/current_version.yaml")
        old_conf["current_version"] = new_version
        old_conf["last_version"] = old_version
        conf_u.overlay_action(r"conf/resource/current_version.yaml", old_conf)
