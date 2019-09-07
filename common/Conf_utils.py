import yaml
import common.File_utils as Pu

# ------------------------------------------------------------------------------
# 配置文件工具
# ------------------------------------------------------------------------------


# 读取配置文件
def read_action(conf_path):
    conf_path = Pu.get_project_path() + conf_path
    return yaml.safe_load(open(conf_path, 'r', encoding='utf-8').read())


# 写入配置文件
def write_action(conf_path, data):
    conf_path = Pu.get_project_path() + conf_path
    return yaml.dump(data, open(conf_path, 'a', encoding='utf-8').read())


# 覆盖配置文件
def overlay_action(conf_path, data):
    conf_path = Pu.get_project_path() + conf_path
    return yaml.dump(data, open(conf_path, 'w', encoding='utf-8').read())
