import os
import logging
import pandas as pd

OUT = "OUT"
ACTION = "action"
FLAG_GO = "flag_go"
DONE = "strategy_done"
ORDERS = "orders"
logger = logging.getLogger(__name__)


def get_balance(path):
    with open(os.path.join(path, 'flag_go'), 'r') as f:
        ret = f.read()
    return ret


def can_i_run(path):
    return os.access(os.path.join(path, 'flag_go'), os.F_OK)


def write_response(path, write):
    with open(os.path.join(path, 'action'), 'w') as f:
        f.write(write)

    with open(os.path.join(path, 'strategy_done'), 'w') as f:
        f.write(' ')


def end_loop(path, response):
    os.remove(path + FLAG_GO)
    try:
        os.remove((path + ORDERS))
    except Exception:
        pass
    write_response(path, response)


def get_orders(path):
    df = pd.DataFrame()
    try:
        df = pd.read_csv(os.path.join(path, ORDERS))
    except FileNotFoundError:
        logger.warning("File is not found, ignore this error if this is the first run ")
    finally:
        return df
