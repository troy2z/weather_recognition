# -*-coding: UTF-8 -*-

import configparser


class Config:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = object.__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        self.conf = configparser.ConfigParser()
        self.conf.read("./conf/app.conf")

    def getString(self, sec, option):
        return self.conf.get(sec, option)

    def getInt(self, sec, option):
        return self.conf.getint(sec, option)

    def getBool(self, sec, option):
        return self.conf.getboolean(sec, option)

    def getFloat(self, sec, option):
        return self.conf.getfloat(sec, option)


conf = Config()

appname = conf.getString('app', 'appname')
host = conf.getString('app', 'host')
port = conf.getString('app', 'port')
upfiles = conf.getString('app', 'upfiles')
debug = conf.getBool('app', 'debug')
