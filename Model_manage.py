from common import *
import importlib
import sys


# ------------------------------------------------------------------------------
# 模块管理
# ------------------------------------------------------------------------------

log = Logger().logger


class Model_manage:
    def __init__(self, running_manage):
        self.current_model = None  # 当前使用的模块
        self.current_model_id = None  # 当前使用的模块名称
        self.current_connect_model = None  # 当前使用的通信模块
        self.rm = running_manage
        self.model_initializer()

    # 模块构造器
    def model_initializer(self, model_id=None):
        try:
            model_manage = conf_u.read_action(r"model/model_manage.yaml")
            if not model_id:
                model_id = model_manage["Model"]["current_model"]
            self.current_model_id = model_id
            model_conf = model_manage["model_list"][self.current_model_id]
            drive_list = conf_u.read_action(r"drive/drive_manage.yaml")["drive_list"]
            drive_import = {}
            for drive in model_conf["model_drive"]:
                drive_import[drive] = self._import_util(drive_list[drive]["drive_path"])
            self.current_connect_model = self._import_util(drive_list[model_conf["model_connect"]][["drive_path"]]).connect_drive(self.rm)
            self.current_model = self._import_util(model_conf["model_path"]).main_model(self.rm, drive_import)
        except KeyError:
            log.error("模块没有找到指定的执行方法")
            log.exception(sys.exc_info())

    def _import_util(self, drive_path):
        if drive_path in sys.modules:
            del sys.modules[drive_path]
        return importlib.import_module(drive_path)

    def quit(self):
        self.current_model.quit_model()
        self.current_connect_model.break_connect()
        self.current_model = None
        self.current_model_id = None
        self.current_connect_model = None



