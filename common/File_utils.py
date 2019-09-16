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


def copy_file(src_file, dst_file):
    try:
        if os.path.isfile(src_file):
            dirname, filename = os.path.split(src_file)
            if not os.path.exists(dst_file):
                os.makedirs(dst_file)
            if os.path.isfile(dst_file + "/" + filename):
                os.remove(dst_file + "/" + filename)
            shutil.move(src_file, dst_file)
    except:
        log.error("复制文件失败")
        log.exception(sys.exc_info())


def del_dir_file(path):
    shutil.rmtree(path)


def run_py_file(py_file):
    res = os.system("python " + py_file)
    return res
