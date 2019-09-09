import os
from common.Log_utils import Logger
import sys
import zipfile
import shutil

# ------------------------------------------------------------------------------
# 文件工具
# ------------------------------------------------------------------------------

log = Logger().logger


# 获取项目根目录
def get_project_path():
    cur_path = os.path.abspath(os.path.dirname(__file__))
    root_path = cur_path[:cur_path.find("lettuce-Sea-v1\\") + len("lettuce-Sea-v1\\")]
    return root_path


def write_file(data, path):
    try:
        len_s = int(len(data) / 2)
        list_nums = []
        for i in range(0, len_s):
            chs = data[2 * i: 2 * i + 2]
            num = int(chs, 16)
            list_nums.append(num)
        bys = bytes(list_nums)
        dirname, filename = os.path.split(path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        f = open(path, "wb")
        f.write(bys)
        f.close()
    except:
        log.error("写入文件失败")
        log.exception(sys.exc_info())


def zip_file(zip_path, res_path):
    zf = zipfile.ZipFile(zip_path)
    try:
        if not os.path.exists(res_path):
            os.makedirs(res_path)
        zf.extractall(path=res_path)
    except:
        log.error("解压文件失败")
        log.exception(sys.exc_info())
    zf.close()


def del_dir_file(path):
    shutil.rmtree(path)


def run_py_file(py_file):
    res = os.system("python " + py_file)
    return res
