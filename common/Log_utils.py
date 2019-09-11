import common.Conf_utils as cu
import logging
from logging import handlers
import os

# ------------------------------------------------------------------------------
# 日志工具
# ------------------------------------------------------------------------------


class Logger:

    _level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }

    def __init__(self):
        self._log_cof = cu.read_action(r"conf/resource/basic_conf.yaml")["Logger"]
        self._log_path = cu.get_project_path() + self._log_cof["log_path"]
        self.logger = logging.getLogger(self._log_path)
        if not os.path.exists(cu.get_project_path() + "LOG"):
            os.mkdir(cu.get_project_path() + "LOG")
        if not self.logger.handlers:
            self._log_init()

    def _log_init(self):
        format_str = logging.Formatter(self._log_cof["fmt"])  # 设置日志格式
        self.logger.setLevel(self._level_relations.get(self._log_cof["level"]))  # 设置日志级别
        sh = logging.StreamHandler()  # 往屏幕上输出
        sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=self._log_path, when=self._log_cof["when"],
                                               backupCount=self._log_cof["back_count"],
                                               encoding='utf-8')  # 往文件里写入#指定间隔时间自动生成文件的处理器
        th.setFormatter(format_str)  # 设置文件里写入的格式
        self.logger.addHandler(sh)  # 把对象加到logger里
        self.logger.addHandler(th)

