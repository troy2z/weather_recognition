# -*-coding: UTF-8 -*-

import logging.config
from logging import handlers

class Loggers:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = object.__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        # 设置输出格式
        formater = logging.Formatter('[%(asctime)s]-[%(levelname)s]-[%(filename)s]-[%(funcName)s:%(lineno)d] : %(message)s')
        # 定义一个日志收集器
        self.logger = logging.getLogger('log')
        # 设定级别
        self.logger.setLevel(logging.DEBUG)
        # 输出渠道一 - 文件形式
        self.fileLogger = handlers.RotatingFileHandler("./logs/app.log", maxBytes=5242880, backupCount=3)

        # 输出渠道二 - 控制台
        self.console = logging.StreamHandler()
        # 控制台输出级别
        self.console.setLevel(logging.DEBUG)
        # 输出渠道对接输出格式
        self.console.setFormatter(formater)
        self.fileLogger.setFormatter(formater)
        # 日志收集器对接输出渠道
        self.logger.addHandler(self.fileLogger)
        self.logger.addHandler(self.console)

    def debug(self, msg):
        self.logger.debug(msg=msg)

    def info(self, msg):
        self.logger.info(msg=msg)

    def warn(self, msg):
        self.logger.warning(msg=msg)

    def error(self, msg):
        self.logger.error(msg=msg)

    def excepiton(self, msg):
        self.logger.exception(msg=msg)

