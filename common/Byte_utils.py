
def byte2int(data):
    return int(data, 16)


def byte2str(data):
    string = ""
    for i in range(0, len(data) // 2):
        string += chr(byte2int(data[(i * 2):(i * 2 + 2)]))
    return string


def int2byte(data, length):
    return ('%0' + str(length) + 'x') % data


def str2byte(data, length):
    by = ""
    for i in range(0, len(data)):
        by += '%02x' % ord(data[i])
    return by.ljust(length, '0')


def plus(data, num):
    return int2byte(byte2int(data) + num, len(data))
