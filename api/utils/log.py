import sys
import time
import logging
from api.utils.method import mkdir
from api.utils import read_yaml
from api.utils import getDir

_config = read_yaml.read_yaml("/config.yaml")


class Logging:
    """setup logging

    Examples:
        >>> import logging
        >>> Logging()
        >>> logging.debug("this is debug message")

    """

    def __init__(self):
        """ settings logging
        """
        """
            第一步，初始化 log 目录
        """
        day_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))  # 2020-12-07

        path = getDir.proDir  # 项目路径

        log_folder = f"{path}/log"

        mkdir(log_folder)

        log_file = f"{log_folder}/{day_time}.log"

        """
            第二步，创建一个handler，用于写入日志文件
        """
        # a 代表继续写log，不覆盖之前log
        # w 代表重新写入，覆盖之前log
        file_handler = logging.FileHandler(log_file, mode='a+')
        file_handler.setLevel(_config['log_level'])

        """
            第三步，再创建一个handler，用于输出到控制台,受配置文件log_level影响
        """
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(_config['log_level'])

        """
            第四步，定义handler的输出格式
        """
        formatter = logging.Formatter(
            "[%(levelname)s - %(asctime)s - %(filename)s ] : %(message)s"
        )
        file_handler.setFormatter(formatter)
        # error_file_handler.setFormatter(formatter)
        stdout_handler.setFormatter(formatter)

        """
            第五步，将logger添加到handler里面
        """
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        logger.handlers = []

        logger.addHandler(file_handler)
        logger.addHandler(stdout_handler)


if __name__ == '__main__':
    Logging()


    def testaaa():
        logging.debug("test")
        logging.error("test")


    testaaa()
