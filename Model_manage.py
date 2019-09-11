from common import *
from drive import *
from model import *


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
        self.init()

    # 初始化模块管理
    def init(self):
        init_conf = conf_u.read_action(r"conf/resource/basic_conf.yaml")["Model"]
        default_model = init_conf["default_model"]
        model_conf = conf_u.read_action(r"model/model_conf.yaml")["model_list"]
        current_model_name = model_conf[default_model]
        self.model_initializer(current_model_name["model_main"])
        self.connect_model_initializer(current_model_name["model_connect"])
        self.current_model_id = current_model_name["model_id"]

        # 模块构造器
    def model_initializer(self, model_name):
        if model_name == "led_bc35g":
            self.current_model = led_bc35g.led_bc35g(self.rm, led.Led(self.rm))

    # 通信模块构造器
    def connect_model_initializer(self, model_name):
        if model_name == "nb_bc35g":
            self.current_connect_model = nb_bc35g.Nb_bc35g.Nb_bc35g(self.rm)

    def quit(self):
        self.current_model.quit_model()
        self.current_connect_model.quit_nb()
        self.current_model = None
        self.current_model_id = None
        self.current_connect_model = None



