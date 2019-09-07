import re

# ------------------------------------------------------------------------------
# Nb模块 bc-35g设备解码器
# ------------------------------------------------------------------------------


class decode:

    command_type = 0
    result_type = 1

    def __init__(self):
        self.order_name = ""  # AT指令名称
        self.order_type = 0  # AT指令类型0命令类1结果类
        self.order_result_p = None  # 匹配接收指令的正则
        self.error_result = None  # AT指令返回信息校验（错误结果）
        self.suc_result = None  # AT指令返回信息校验（正确结果）

        self.error = re.compile('ERROR')  # 普通消息失败
        self.ok = re.compile('OK')  # 普通消息成功

        self.result = None  # 返回结果
        self.status = 0  # 执行结果（0未执行1执行失败2执行成功）

    # 命令类
    def command_cla(self, order_name, order_result=None):
        self.order_name = order_name
        self.order_result_p = re.compile(order_name)
        if order_result:
            self.order_result_p = re.compile(order_result)
        self.order_type = self.command_type
        return self

    # 结果类
    def result_cla(self, order_name, order_result=None, error_result=None, suc_result=None):
        self.order_name = order_name
        self.order_result_p = re.compile(order_name)
        if order_result:
            self.order_result_p = re.compile(order_result)
        self.order_type = self.result_type
        self.error_result = error_result
        self.suc_result = suc_result
        return self

    # 是否命中当前解码器
    def is_hit(self, at_result):
        # 如果此编码器为命令类，只校验OK/ERROR
        # 如果此编码器为结果类，将结果放置成员变量，根据调用方法返回相关操作
        while self.result:
            pass
        if self.error.search(at_result):
            self.result = at_result
            self.status = 1
            return True
        elif self.order_type == self.command_type:
            if self.ok.search(at_result):
                self.result = at_result
                self.status = 2
                return True
        elif self.order_type == self.result_type:
            if self.order_result_p.search(at_result):
                self.result = at_result.split(":")[1]
                return True
        return False

    # 获取执行结果
    def get_order_status(self):
        while not self.result:
            pass
        if self.status == 1:
            self._result_clean()
            return False
        if self.order_type == self.command_type:
            status, result = self._result_clean()
            return bool(status - 1)
        elif self.order_type == self.result_type:
            if self.error_result:
                self.status = int(self.error_result != self.result) + 1
                status, result = self._result_clean()
                return status == 2
            elif self.suc_result:
                self.status = int(self.suc_result == self.result) + 1
                status, result = self._result_clean()
                return status == 2
            else:
                self._result_clean()

    # 获取内容
    def get_order_result(self):
        while not self.result:
            pass
        if self.status == 1:
            self._result_clean()
            return None
        status, result = self._result_clean()
        return result

    def _result_clean(self):
        result = self.result
        status = self.status
        self.result = None
        self.status = 0
        return status, result



