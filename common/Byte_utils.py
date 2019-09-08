
def byte2int(data):
    return int(data, 16)


def byte2str(data):
    string = ""
    for i in range(0, len(data) // 2):
        res = byte2int(data[(i * 2):(i * 2 + 2)])
        if res == 0:
            continue
        string += chr(res)
    return string


def int2byte(data, length):
    return ('%0' + str(length) + 'x') % data


def str2byte(data, length):
    by = ""
    for i in range(0, len(data)):
        by += '%02x' % ord(data[i])
    return by.ljust(length, '0')


def byte2bytes(data):
    len_s = int(len(data) / 2)
    list_nums = []
    for i in range(0, len_s):
        chs = data[2 * i: 2 * i + 2]
        num = int(chs, 16)
        list_nums.append(num)
    return bytes(list_nums)


def plus(data, num):
    return int2byte(byte2int(data) + num, len(data))
