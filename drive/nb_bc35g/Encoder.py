
# ------------------------------------------------------------------------------
# Nb模块 bc-35g设备编码器
# ------------------------------------------------------------------------------


class encoder:

    query = "?"
    execute = "="

    def __init__(self, order_name, order_identify=None, data=None, retry=1):
        self.order_name = order_name
        self.order_identify = order_identify
        self.data = data
        self._retry = retry

    # 构建AT指令
    def get_at_order(self):
        at_order = "AT"
        if self.order_name:
            at_order += "+" + self.order_name
            if self.order_identify:
                at_order += self.order_identify
                if self.data:
                    for d in self.data:
                        at_order += str(d)
        at_order += '\n'
        return at_order

    # 是否重试
    def is_retry(self):
        return self._retry != 0

    # 一次流程后调用
    def flow(self):
        self._retry -= 1
