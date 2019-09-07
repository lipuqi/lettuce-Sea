import os

# ------------------------------------------------------------------------------
# 文件工具
# ------------------------------------------------------------------------------


# 获取项目根目录
def get_project_path():
    cur_path = os.path.abspath(os.path.dirname(__file__))
    root_path = cur_path[:cur_path.find("lettuce-Sea-v1\\") + len("lettuce-Sea-v1\\")]
    return root_path
