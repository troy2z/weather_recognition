# -*-coding: UTF-8 -*-
import os
import time
import random
import string
import pandas as pd


class Comm:
    __instance = None

    def __init__(self):
        pass

    def generate_random_str(randomlength=16):
        """
        生成一个指定长度的随机字符串，其中
        string.digits=0123456789
        string.ascii_letters=abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
        """
        str_list = [random.choice(string.digits + string.ascii_letters) for i in range(randomlength)]
        random_str = ''.join(str_list)
        return random_str

    def ftypelist(self):
        return [
            ".jpeg",
            ".png",
            ".gif",
            ".jpg",
            ".bmp"
        ]

    # 支持文件类型
    # 用16进制字符串的目的是可以知道文件头是多少字节
    # 各种文件头的长度不一样，少半2字符，长则8字符
    def typeList(self):
        return {
            "3c68313ee689abe68f8f": 'html',
            "504b03040a0000000000": 'xlsx',
            '504b0304140008080800': 'docx',
            "d0cf11e0a1b11ae10000": 'doc',
            '2d2d204d7953514c2064': 'sql',
            'ffd8ffe000104a464946': 'jpg',
            '89504e470d0a1a0a0000': 'png',
            '47494638396126026f01': 'gif',
            '3c21444f435459504520': 'html',
            '3c21646f637479706520': 'htm',
            '48544d4c207b0d0a0942': 'css',
            '2f2a21206a5175657279': 'js',
            '255044462d312e350d0a': 'pdf',
        }

    # 字节码转16进制字符串
    def bytes2hex(self, bytes):
        num = len(bytes)
        hexstr = u""
        for i in range(num):
            t = u"%x" % bytes[i]
            if len(t) % 2:
                hexstr += u"0"
            hexstr += t
        return hexstr.upper()

    def createDir(self, root_dir):
        localtime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        # 系统当前时间年份
        year = time.strftime('%Y', time.localtime(time.time()))
        # 月份
        month = time.strftime('%m', time.localtime(time.time()))
        # 日期
        day = time.strftime('%d', time.localtime(time.time()))
        # 具体时间 小时分钟毫秒
        mdhms = time.strftime('%m%d%H%M%S', time.localtime(time.time()))
        full_path = os.path.join(root_dir, localtime)

        if not os.path.exists(full_path):
            os.mkdir(full_path)

        return full_path


comm = Comm()
ftypelist = comm.ftypelist()
