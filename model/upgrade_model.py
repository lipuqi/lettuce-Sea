from common import *
import sys

log = Logger().logger


class upgrade_model:
    def __init__(self, upgrade_path, install_list):
        self.up = upgrade_path
        self.drive_m = conf_u.read_action(r"drive/drive_manage.yaml")
        self.model_m = conf_u.read_action(r"model/model_manage.yaml")
        self.install_list = install_list

    def execute_upgrade(self):
        model_path = conf_u.get_project_path() + 'model/'
        try:
            for model in self.install_list:
                name = model["name"]
                version = model["version"]
                main_path = model["main_path"]
                model_drive = model["model_drive"]
                if model["connect"] not in self.drive_m["drive_list"]:
                    log.error("安装模块失败！模块没有 " + model["connect"] + " 通信驱动，请先安装")
                    return False

                for md in model_drive:
                    if md not in self.drive_m["drive_list"]:
                        log.error("安装模块失败！模块没有 " + md + " 驱动，请先安装")
                        return False

                is_continue = False
                for i in range(0, len(self.model_m["model_list"])):
                    if name == self.model_m["model_list"][i]["model_name"]:
                        if version == self.model_m["model_list"][i]["model_version"]:
                            is_continue = True
                            break
                        del self.model_m["model_list"][i]
                        break

                if is_continue:
                    continue

                new_model = {}
                new_model["model_name"] = name
                new_model["model_version"] = version
                new_model["model_connect"] = model["connect"]
                new_model["model_path"] = main_path
                new_model["model_drive"] = model_drive
                self.model_m["model_list"].append(new_model)

                for file in model["file"]:
                    file_u.copy_file(self.up + "/" + name + "/" + file, model_path + name)

                conf_u.overlay_action(r"model/model_manage.yaml", self.model_m)

        except:
            log.error("升级模块失败")
            log.exception(sys.exc_info())
            return False
        return True
