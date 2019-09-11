import yaml
import os

# ------------------------------------------------------------------------------
# 配置文件工具
# ------------------------------------------------------------------------------


# 获取项目根目录
def get_project_path():
    return r"/home/pi/lettuce-Sea"


# 读取配置文件
def read_action(conf_path):
    conf_path = get_project_path() + conf_path
    r = open(conf_path, 'r', encoding='utf-8')
    result = r.read()
    r.close()
    return yaml.safe_load(result)


# 写入配置文件
def write_action(conf_path, data):
    conf_path = get_project_path() + conf_path
    r = open(conf_path, 'a', encoding='utf-8')
    yaml.dump(data, r)
    r.close()


# 覆盖配置文件
def overlay_action(conf_path, data):
    conf_path = get_project_path() + conf_path
    r = open(conf_path, 'w', encoding='utf-8')
    yaml.dump(data, r)
    r.close()
