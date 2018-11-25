import logging
from logging.config import fileConfig

from os import path

log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging_config.ini')
logging.config.fileConfig(log_file_path)
logger = logging.getLogger(__name__)

import threading
from config.config import config
from strategy.strategy import Strategy
from webserver.app import run

CROSSES = ["EURUSD_"]

if __name__ == "__main__":
    logger.info(' Started APP')
    d = {}

    # Start Thread for each strategy
    for c in CROSSES:
        conf = config[c]
        s = Strategy(c, conf)
        th = threading.Thread(target=s.run)
        th.start()
        d[c.replace('_', '')] = s

    th = threading.Thread(target=run, args=(d,))
    th.start()
