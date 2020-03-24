"""Application constants file
"""
import os

APP_LOG_FORMAT = "[%(asctime)s %(filename)s:%(lineno)s %(levelname)-2s %(funcName)20s()] %(message)s"
APP_PATH = os.path.dirname(os.path.abspath(__file__))
APP_PATH = APP_PATH.replace("config", "")
APP_LOG_FILENAME = APP_PATH + "log/application.log"
