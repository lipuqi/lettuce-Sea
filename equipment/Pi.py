import sys
import time
"""
基础操作
"""


class Pi:
    def __init__(self, mSerial, receiveMsg, nmgs, csq, cfun, cgatt, qlwuldataex, nconfig, nrb, gpio_equipment):
        super(Pi, self).__init__()
        self.mid = None
        self.mSerial = mSerial
        self.receiveMsg = receiveMsg
        self.nmgs = nmgs
        self.csq = csq
        self.cfun = cfun
        self.cgatt = cgatt
        self.qlwuldataex = qlwuldataex
        self.nconfig = nconfig
        self.nrb = nrb
        self.gpio_equipment = gpio_equipment

    # 系统初始化
    def sys_init(self, index=0):
        # 如果重试3次皆失败，判定初始化失败
        if index == 3:
            return 2
        print("开始初始化")
        self.cfun.execute_at("1")  # 开启射频
        self.csq.execute_at()  # 查询信号
        time.sleep(5)
        cg_res = self.cgatt.integration_at("1")  # 入网
        # 查看入网是否成功
        if cg_res == 2:
            print("初始化遇到问题，开始默认初始化")
            self.nconfig.execute_at("AUTOCONNECT,FALSE")  # 手动入网模式
            self.nrb.execute_at()  # 重启
            index += 1
            self.sys_init(index)  # 递归
        print("结束初始化")
        return 1

    # 退出命令
    def execute_quit(self):
        print("执行退出")
        suc = "07" + self.mid + "0000"  # 成功响应
        self.nmgs.execute_at(suc)  # 发送响应指令
        self.gpio_equipment.execute_cleanup()  # 关闭gpio口
        self.qlwuldataex.execute_at("3,AA34BB,0x0001")  # 发送释放RRC
        self.cfun.execute_at("0")  # 关闭射频，保存频点
        time.sleep(20)  # 保持20秒时间，充分保证模组的正常退出
        self.receiveMsg.set_quit_sys()  # 全体线程置为退出位
        self.mSerial.port_close()  # 关闭串口连接
        print("退出！")
        time.sleep(10)  # 保证所有线程已经退出
        sys.exit()  # 程序退出

    # 上报心跳线程方法
    def heartbeat_examine(self):
        second = 0
        while self.receiveMsg.quit_sys == 0:
            # 每2分钟上报一次
            if second < 20:
                time.sleep(6)  # 这里之所以设6是因为设短时间延时利于及时退出
                second += 1
            else:
                result = self.nmgs.execute_at("0501")
                if result == 1:
                    second = 0

    # 保存命令响应码
    def set_mid(self, mid):
        self.mid = mid
