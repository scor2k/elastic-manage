# -*- coding: UTF-8 -*-

import logging
import json
import sys
import os
import pkg_resources

from datetime import datetime

logger = logging.getLogger()

DEBUG = os.environ.get("DEBUG", False)
WARNING = os.environ.get("WARNING", True)

version = pkg_resources.require("elastic-manage")[0].version

class sreLogs:
    APP = None

    def __init__(self):
        pass

    def info(self, msg, **kwargs):
        tmp = {}
        tmp["timestamp"] = str(datetime.utcnow()) + " UTC"
        tmp["version"] = version
        tmp["level"] = "info"

        tmp["msg"] = msg

        try:
            if kwargs is not None:
                for key, value in kwargs.items():
                    tmp[key] = str(value)
        except:
            pass

        try:
            logger.warning(json.dumps(tmp))
        except:
            print("---- INFO ----------------------")
            print(tmp)
            print("----- E N D ----------------")

    def error(self, msg, **kwargs):
        tmp = {}
        tmp["timestamp"] = str(datetime.utcnow()) + " UTC"
        tmp["version"] = version
        tmp["level"] = "error"

        tmp["msg"] = msg

        try:
            if kwargs is not None:
                for key, value in kwargs.items():
                    tmp[key] = str(value)
        except:
            pass

        try:
            logger.warning(json.dumps(tmp))
        except:
            print("---- ERROR ----------------------")
            print(tmp)
            print("----- E N D ----------------")

    def warning(self, msg, **kwargs):
        if not WARNING:
            return True
        tmp = {}
        tmp["timestamp"] = str(datetime.utcnow()) + " UTC"
        tmp["version"] = version
        tmp["level"] = "warning"

        tmp["msg"] = msg

        try:
            if kwargs is not None:
                for key, value in kwargs.items():
                    tmp[key] = str(value)
        except:
            pass

        try:
            logger.warning(json.dumps(tmp))
        except:
            print("---- WARNING ----------------------")
            print(tmp)
            print("----- E N D ----------------")

    def debug(self, msg, **kwargs):
        if not DEBUG:
            return True

        tmp = {}
        tmp["timestamp"] = str(datetime.utcnow()) + " UTC"
        tmp["version"] = version
        tmp["level"] = "debug"

        tmp["msg"] = msg

        try:
            if kwargs is not None:
                for key, value in kwargs.items():
                    tmp[key] = str(value)
        except:
            pass

        try:
            logger.warning(json.dumps(tmp))
        except:
            print("---- DEBUG ----------------------")
            print(tmp)
            print("----- E N D ----------------")
