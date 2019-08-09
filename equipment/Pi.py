import sys
import time


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

    def sys_init(self, index=1):
        if index == 4:
            return 2
        print("开始初始化")
        self.cfun.execute_at("1")
        time.sleep(5)
        self.csq.query_at()
        self.cgatt.execute_at("1")
        time.sleep(10)
        cg_res = self.cgatt.query_at()
        if cg_res == 2:
            print("初始化遇到问题，开始默认初始化")
            self.nconfig.execute_at("AUTOCONNECT,FALSE")
            self.nrb.execute_at()
            index += 1
            self.sys_init(index)
        print("结束初始化")
        return 1

    def execute_quit(self):
        print("执行退出")
        suc = "07" + self.mid + "0000"
        self.nmgs.execute_at(suc)
        self.gpio_equipment.execute_cleanup()
        self.qlwuldataex.execute_at("3,AA34BB,0x0001")
        time.sleep(20)
        self.cfun.execute_at("0")
        self.receiveMsg.set_quit_sys()
        self.mSerial.port_close()
        sys.exit()
        print("退出！")

    def heartbeat_examine(self):
        second = 0
        while self.receiveMsg.quit_sys == 0:
            # 2分钟
            if second < 20:
                time.sleep(6)
                second += 1
            else:
                result = self.nmgs.execute_at("0501")
                if result == 1:
                    second = 0

    def set_mid(self, mid):
        self.mid = mid
