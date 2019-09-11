import os
from common import *
import sys
import zipfile
import shutil

# ------------------------------------------------------------------------------
# 文件工具
# ------------------------------------------------------------------------------

log = Logger().logger


def write_file(data, path):
    try:
        dirname, filename = os.path.split(path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        f = open(path, "wb")
        f.write(data)
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
