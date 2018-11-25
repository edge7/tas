import os
import threading
import warnings
import time
from datetime import datetime
import logging

from utility.send_nots import notify

logger = logging.getLogger(__name__)
import pandas as pd

from discovery.discovery import in_pips, macds, search_for_bullish_and_bearish_candlestick, rsi_strategy, get_pips
from market_info.market_info import MarketInfo
from utility.adjust import adjust_data, adjust_data_daily
from utility.mql4_socket import can_i_run, ACTION, get_balance, get_orders, end_loop

warnings.filterwarnings("ignore")

PATH_ = "/home/edge7/Downloads/mql4/"


def get_info(df, CROSS):
    mi = MarketInfo(df, CROSS)
    mi.search_for_info()
    return mi


def insert_balance(b, ba):
    if len(ba) >= 15500:
        ba = ba[1:]
    ba.append(b)
    return ba


class Strategy(object):
    def __init__(self, CROSS, config):
        self.CROSS = CROSS
        self.PATH = PATH_
        self.send_email = False
        self.config = config
        self.start = True
        self.lock = threading.Lock()
        self.macd_signals = []
        self.objects = None
        self.bullish_candles = ""  # Return by API
        self.bearish_candles = ""  # Return by API
        self.trade = True
        self.notify = False

    def get_avg(self, window=50):
        p = self.df_4hour[self.CROSS + "CLOSE"].iloc[-1]
        avg = self.df_4hour[self.CROSS + "CLOSE"].rolling(window = window).mean().iloc[-1]
        return round( get_pips(self.CROSS, p - avg), 4)

    def get_orders(self):
        return self.orders

    def get_last_close(self):
        return self.df_1hour[self.CROSS + "CLOSE"].iloc[-1]

    # serivce-bearish/bullish-descrizione
    def get_trend_line(self, bearish=False):
        trends = self.objects[self.objects["Type"] == "TREND"]
        res = []
        for index, row in trends.iterrows():
            name = row['name']
            if bearish and 'bullish' in name:
                continue
            if not bearish and 'bearish' in name:
                continue
            name = name.replace('service.', "")
            diff = row['dist']
            diff = float(diff)
            diff = get_pips(self.CROSS, diff)
            diff = round(diff, 2)
            res.append({'name': str(name), 'dist': diff})
        return res

    def get_lines(self, bearish=False):
        lines = self.objects[self.objects["Type"] == "HLINE"]
        res = []
        for index, row in lines.iterrows():
            name = row['name']
            if bearish and 'bullish' in name:
                continue
            if not bearish and 'bearish' in name:
                continue
            name = name.replace('service.', "")
            diff = row['dist']
            diff = float(diff)
            diff = get_pips(self.CROSS, diff)
            diff = round(diff, 2)
            res.append({'name': str(name), 'dist': diff})
        return res

    def get_bearish_candles(self, notifa=False):
        res = ""
        if len(list(self.bearish.keys())) > 1:
            for key, value in self.bearish.items():
                if key == 'datetime':
                    continue
                res += str(key) + " - " + str(value)
        if res != "":
            self.bearish_candles = res
            if notifa:
                notify(str(res), self.CROSS)

        return self.bearish_candles

    def get_bullish_candles(self, notifa=False):
        res = ""
        if len(list(self.bullish.keys())) > 1:
            for key, value in self.bullish.items():
                if key == 'datetime':
                    continue
                res += str(key) + " - " + str(value)
        if res != "":
            self.bullish_candles = res
            if notifa:
                notify(res, self.CROSS)

        return self.bullish_candles

    def get_last_signals_macd(self):
        s = ""
        for item in self.macd_signals:
            trigger = item[0]
            trigger = round(trigger, 3)
            action = item[1]
            t = item[2]
            s += str(trigger) + " - " + str(action) + " - " + str(t)
        return s

    def run(self):
        logger.info(self.CROSS + " is starting ")
        balances = []
        while True:
            # FLAG_GO
            while not can_i_run(self.PATH):
                time.sleep(0.1)

            try:
                os.remove(self.PATH + ACTION)
            except Exception:
                pass
            si = True
            while si:
                try:
                    balance = get_balance(self.PATH)
                    var = balance.split(',')[1]
                    si = False
                except Exception:
                    pass

            balances = insert_balance(balance, balances)
            self.orders = get_orders(self.PATH)
            df = pd.read_csv(self.PATH + 'o.csv', sep=",").tail(800).reset_index(drop=True)
            df["TIME"] = df["TIME"].apply(lambda x: datetime.strptime(x, '%Y.%m.%d %H:%M'))
            self.df_1hour = df.copy()
            self.df_4hour = adjust_data(df, self.CROSS)
            self.objects = pd.read_csv(self.PATH + 'objects')
            if df.shape[0] < 60:
                end_loop(self.PATH, "OUT")
                continue

            market_info = get_info(self.df_4hour, self.CROSS)
            self.bearish, self.bullish = search_for_bullish_and_bearish_candlestick(market_info)

            if self.notify:
                self.get_bearish_candles(notifa=True)
                self.get_bullish_candles(notifa=True)

            # Start Calling different Strategies
            if 'macd' in self.config.keys():
                param = self.config['macd']
                trigger, tp, sl, action, close = macds(self.df_1hour, self.orders, self.df_4hour, self.CROSS, param)
                self.update_macd_signals(trigger, action, notifa=self.notify)

            if 'rsi' in self.config.keys():
                param = self.config['rsi']
                trigger, tp, sl, action, close = rsi_strategy(self.df_1hour, self.orders, self.df_4hour, self.CROSS, param)

            response = str(trigger) + "," + str(tp) + "," + str(sl) + "," + str(action)

            if close is not None:
                response = close
            if trigger is not None or close is not None:
                response = response + "," + str(in_pips(100, self.CROSS))
                logger.info(response)

            if not self.trade:
                response = "OUT"

            end_loop(self.PATH, response)

    def update_macd_signals(self, trigger, action, notifa=False):
        if trigger is not None:
            self.macd_signals.append((trigger, action, datetime.now().strftime("%Y-%m-%d %H:%M")))
            if len(self.macd_signals) > 1:
                self.macd_signals = self.macd_signals[1:]

            if notifa:
                notify("MACD: " + self.get_last_signals_macd(), self.CROSS )

