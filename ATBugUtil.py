from SerialPort import SerialPort
from ReceiveMsg import ReceiveMsg
from AT.NNMI import NNMI
from AT.QLWEVTIND import QLWEVTIND
from AT.NMGS import NMGS
from AT.CFUN import CFUN
from AT.CGATT import CGATT
from AT.QLWULDATAEX import QLWULDATAEX
from AT.CSQ import CSQ
from AT.NCONFIG import NCONFIG
from AT.NRB import NRB
from equipment.Led import Led
from equipment.Gpio import Gpio
from equipment.Pi import Pi
from equipment.Drive import Drive
import threading

serialPort = "/dev/ttyAMA0"  # 串口
'''serialPort = "COM3"  # 串口'''
baudRate = 9600  # 波特率

"""
所有模块初始化
"""
nnmi = NNMI()
qlwevtind = QLWEVTIND()
mSerial = SerialPort(serialPort, baudRate)
receiveMsg = ReceiveMsg(mSerial, nnmi, qlwevtind)

nmgs = NMGS(mSerial, receiveMsg)
csq = CSQ(mSerial, receiveMsg)
cfun = CFUN(mSerial, receiveMsg)
cgatt = CGATT(mSerial, receiveMsg)
qlwuldataex = QLWULDATAEX(mSerial, receiveMsg)
nconfig = NCONFIG(mSerial, receiveMsg)
nrb = NRB(mSerial, receiveMsg)

gpio_equipment = Gpio()
led_equipment = Led(gpio_equipment, nmgs)
pi_equipment = Pi(mSerial, receiveMsg, nmgs, csq, cfun, cgatt, qlwuldataex, nconfig, nrb, gpio_equipment)
drive = Drive(nnmi, receiveMsg, led_equipment, pi_equipment)

if __name__ == '__main__':
    t1 = threading.Thread(target=receiveMsg.receive_data)
    t2 = threading.Thread(target=drive.order_monitor)
    t3 = threading.Thread(target=pi_equipment.heartbeat_examine)
    t1.start()  # 开启接收信息的线程
    t2.start()  # 开启监听待处理命令的线程
    in_res = pi_equipment.sys_init()  # 执行初始化
    # 初始化失败退出，没有失败则开启心跳上报
    if in_res == 2:
        print("初始化失败，现进入退出阶段")
        pi_equipment.execute_quit()
    else:
        t3.start()  # 开启心跳上报线程
