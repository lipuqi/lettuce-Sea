from common import *
import sys

log = Logger().logger


class upgrade_drive:
    def __init__(self, upgrade_path, install_list):
        self.up = upgrade_path
        self.drive_m = conf_u.read_action(r"drive/drive_manage.yaml")
        self.install_list = install_list

    def execute_upgrade(self):
        drive_path = conf_u.get_project_path() + 'drive/'
        try:
            for drive in self.install_list:
                name = drive["name"]
                version = drive["version"]
                main_path = drive["main_path"]
                if name in self.drive_m["drive_list"]:
                    if self.drive_m["drive_list"][name]["version"] == version:
                        continue
                    self.drive_m["drive_list"][name]["version"] = version
                    self.drive_m["drive_list"][name]["drive_path"] = main_path
                else:
                    self.drive_m["drive_list"][name] = {}
                    self.drive_m["drive_list"][name]["version"] = version
                    self.drive_m["drive_list"][name]["drive_path"] = main_path

                for file in drive["file"]:
                    file_u.copy_file(self.up + "/" + name + "/" + file, drive_path + name)

                conf_u.overlay_action(r"drive/drive_manage.yaml", self.drive_m)
        except:
            log.error("升级驱动失败")
            log.exception(sys.exc_info())
            return False
        return True
