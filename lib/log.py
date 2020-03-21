import Database.constants as CONST
import logging


class Log:
    """
    This class encapsulates logging functionality.
    """

    initialized = False
    logger = None

    def __init__(self):
        pass

    @staticmethod
    def initialize(context, level):
        """
        This method is used to do application logging configuration.
        """
        if not Log.initialized:
            Log.logger = logging.getLogger(context)
            Log.initialized = True
            logging.basicConfig(
                filename=CONST.APP_LOG_FILENAME,
                format=CONST.APP_LOG_FORMAT,
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            Log.logger.setLevel(level)
            Log.logger.log(50, 'Logging initialised, level={}'.format(level))
        return Log.logger

    @staticmethod
    def str(x):
        """
        This method is used to get the substring of the given string more specifically x.
        """
        return str(x)[:200]

    @staticmethod
    def get_logger(context):
        """
        This method is used to get the instance of a particular job jog file.
        """
        Log.job_log = logging.getLogger(context)
        return Log.job_log


log = Log.initialize(__name__, level=logging.INFO)
