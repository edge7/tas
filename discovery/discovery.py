import datetime

from dateutil.parser import parse


def get_pips(CROSS, body):
    if 'JPY' in CROSS or 'XAU' in CROSS or 'XAG' in CROSS:
        multiply = 100.0
    else:
        multiply = 10000.0
    return body * multiply

def in_pips(param, CROSS):
    if 'JPY' in CROSS or 'XAU' in CROSS or 'XAG' in CROSS:
        multiply = 100.0
    else:
        multiply = 10000.0
    return param / multiply


def avg(df, CROSS, window=50):
    last_price = df[CROSS + "CLOSE"].iloc[-1]
    last_avg = df[CROSS + "CLOSE"].rolling(window=window).mean().iloc[-1]
    if last_price >= last_avg:
        return "BUY"
    return "SELL"


def search_for_bullish_and_bearish_candlestick(market_info):
    bearish = {'datetime': str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))}
    bullish = {'datetime': str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))}
    market_info = market_info.candle_info
    # Hammer is bullish
    if market_info.hammer:
        bullish['hammer'] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    # Hanging man is bearish
    if market_info.hanging:
        bearish['hanging'] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

    if market_info.inverted_hammer:
        bullish['inv_hammer'] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

    if market_info.shooting_start:
        bearish['shooting_star'] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

    if market_info.bullish_engulfing:
        bullish['bullish_eng'] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

    if market_info.bearish_engulfing:
        bearish['bearish_eng'] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

    if market_info.tweezer_tops:
        bullish['tweezer_tops'] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

    if market_info.tweezer_bottoms:
        bearish['tweezer_bottoms'] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

    if market_info.morning_star:
        bullish['morning_star'] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

    if market_info.evening_star:
        bearish['evening_star'] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

    if market_info.three_white:
        bullish['3_white'] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

    if market_info.three_black:
        bearish['3_black'] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

    if market_info.three_ins_up:
        bullish['3_ins_up'] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

    if market_info.three_ins_down:
        bearish['3_ins_down'] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

    if market_info.marubozu is not None:
        if market_info.marubozu == 'white':
            bullish['marubozu'] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        else:
            bearish['marubozu'] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

    return bearish, bullish


def optimize_macd(df, CROSS, w1, w2, ac):
    import numpy as np
    import pandas as pd
    df = df.copy()
    l = df.shape[0]
    if ac == "SELL":
        r = np.arange(0, -0.01, -0.0003)
    else:
        r = np.arange(0, 0.01, 0.0003)

    risultati = {}
    for soglia in r:
        for i in range(50, l - 16):
            tmp = df.iloc[0:i + 1]
            res = macd(tmp, CROSS, window1=w1, window2=w2, soglia=soglia)
            if ac == "BUY":
                if res == ac:
                    dist = -tmp.iloc[-1][CROSS + "CLOSE"] + df.iloc[i + 15][CROSS + "CLOSE"]
                    if soglia in risultati:
                        risultati[soglia].append(dist)
                    else:
                        risultati[soglia] = [dist]
            if ac == "SELL":
                if res == ac:
                    dist = tmp.iloc[-1][CROSS + "CLOSE"] - df.iloc[i + 15][CROSS + "CLOSE"]
                    if soglia in risultati:
                        risultati[soglia].append(dist)
                    else:
                        risultati[soglia] = [dist]
    calc = []
    for item, key in risultati.items():
        m = pd.Series(key).mean()
        calc.append((item, m))

    calc = sorted(calc, key=lambda tup: tup[1], reverse=True)
    if len(calc) < 2:
        calc = [[0], [0]]
    print("------")
    print(ac)
    print(risultati)
    print(calc)
    print(calc[0])
    print("----")
    res = round((calc[0][0] + calc[1][0]) / 2.0, 4)
    print("Return: " + str(res))
    return res


def macd(df, CROSS, window1=14, window2=26, final_avg=9, soglia=0):
    short = df[CROSS + "CLOSE"].ewm(span=window1).mean()
    long = df[CROSS + "CLOSE"].ewm(span=window2).mean()
    diff = short - long
    diff = diff.ewm(span=final_avg).mean()
    d1 = diff.iloc[-1]
    d2 = diff.iloc[-2]
    if d1 > soglia and d2 < soglia:
        return "BUY"
    if d1 < soglia and d2 > soglia:
        return "SELL"


def macd_info(df, CROSS, window1=14, window2=26, final_avg=9):
    short = df[CROSS + "CLOSE"].ewm(span=window1).mean()
    long = df[CROSS + "CLOSE"].ewm(span=window2).mean()
    diff = short - long
    diff = diff.ewm(span=final_avg).mean()
    d1 = diff.iloc[-1]
    if d1 > 0:
        return "BUY"
    if d1 < 0:
        return "SELL"


soglia = {}
counter = 0


def macds(df, orders, df_4hour, CROSS, conf):
    global last_pos
    global soglia
    global counter
    trigger = tp = sl = action = close = None
    df = df.copy()
    window1_4h = conf['window1_4h']
    window2_4h = conf['window2_4h']
    final_avg_4h = conf['final_avg_4h']

    window1_1h = conf['window1_1h']
    window2_1h = conf['window2_1h']
    final_avg_1h = conf['final_avg_1h']

    if not orders.empty:
        while not orders.empty and close is None:

            try:
                seconds_bars = (df["TIME"].iloc[-1] - df["TIME"].iloc[
                    -2]).total_seconds()

            except Exception:
                seconds_bars = 1

            if seconds_bars == 0: seconds_bars = 1
            seconds_from_orders = (df["TIME"].iloc[-1] - parse(
                orders['TIME'].iloc[-1])).total_seconds()
            bar_ago = int(seconds_from_orders / seconds_bars) + 1
            id = str(orders["ID"].iloc[-1])
            lots = str(orders["LOTS"].iloc[-1])
            profit = orders["PROFIT"].iloc[-1]
            day = df["TIME"].iloc[-1].date()

            if bar_ago > 15 and profit != 0:
                close = 'CLOSE,' + id + "," + str(lots)

            if close is None and bar_ago > 3 and bar_ago % 10 == 0 and profit > 0:
                lots_ = lots
                lots = float(lots) / 4.0
                lots = round(lots, 3)
                if lots == 0:
                    lots = lots_
                close = 'CLOSE,' + id + "," + str(lots)

            if bar_ago > 15 and profit == 0:
                close = 'CLOSE,' + id + "," + str(lots)

            orders = orders.iloc[:-1]

    else:
        p = df[CROSS + "CLOSE"].iloc[-1]
        action = macd_info(df_4hour, CROSS, window1=window1_4h, window2=window2_4h, final_avg=final_avg_4h)
        if soglia.get(action, None) is None or counter > 150:
            s = optimize_macd(df, CROSS, w1=window1_1h, w2=window2_1h, ac=action)
            soglia[action] = s
            counter = 0
        counter += 1
        s = soglia[action]
        r = macd(df, CROSS, window1=window1_1h, window2=window2_1h, final_avg=final_avg_1h, soglia=s)

        if r != action:
            action = None

        TP = conf['TP']
        SL = conf['SL']

        if action == "SELL":
            trigger = p - in_pips(3, CROSS)
            p = trigger
            tp = p - in_pips(TP, CROSS)
            sl = p + in_pips(SL, CROSS)
            last_pos = action

        if action == "BUY":
            trigger = p + in_pips(3, CROSS)
            p = trigger
            tp = p + in_pips(TP, CROSS)
            sl = p - in_pips(SL, CROSS)
            last_pos = action

    if tp is None:
        action = None
    return trigger, tp, sl, action, close


def rsi_info(df_copy, CROSS, period, thre_buy, thre_sell):
    def avg_gain(l):
        g = 0.00001
        for i in l:
            if i > 0:
                g += i
        return g

    def avg_loss(l):
        g = 0.00001
        for i in l:
            if i < 0:
                g += abs(i)
        return g

    df_copy["AVG_GAIN"] = df_copy[CROSS + "BODY"].rolling(window=period).apply(lambda l: avg_gain(l)) / period
    df_copy["AVG_LOSS"] = df_copy[CROSS + "BODY"].rolling(window=period).apply(lambda l: avg_loss(l)) / period
    df_copy["RSI"] = 100 - 100 / (1 + df_copy["AVG_GAIN"] / df_copy["AVG_LOSS"])
    last_value = df_copy['RSI'].iloc[-2]
    ultimo = df_copy['RSI'].iloc[-1]
    if last_value <= thre_buy <= ultimo:
        return "BUY"
    if last_value >= thre_sell >= ultimo:
        return "SELL"

    return "NONE"


def rsi_strategy(df, orders, df_4hour, CROSS, conf):
    global last_pos
    trigger = tp = sl = action = close = None
    df = df.copy()
    period_1h = conf['period_1h']
    avg_4h = conf['avg_4h']
    thre_buy = conf['thre_buy']
    thre_sell = conf['thre_sell']

    if not orders.empty:
        while not orders.empty and close is None:

            try:
                seconds_bars = (df["TIME"].iloc[-1] - df["TIME"].iloc[
                    -2]).total_seconds()

            except Exception:
                seconds_bars = 1

            if seconds_bars == 0: seconds_bars = 1
            seconds_from_orders = (df["TIME"].iloc[-1] - parse(
                orders['TIME'].iloc[-1])).total_seconds()
            bar_ago = int(seconds_from_orders / seconds_bars) + 1
            id = str(orders["ID"].iloc[-1])
            lots = str(orders["LOTS"].iloc[-1])
            profit = orders["PROFIT"].iloc[-1]

            if bar_ago > 100 and profit > 0:
                close = 'CLOSE,' + id + "," + str(lots)

            if close is None and bar_ago > 3 and bar_ago % 5 == 0 and profit > 0:
                lots_ = lots
                lots = float(lots) / 4.0
                lots = round(lots, 3)
                if lots == 0:
                    lots = lots_
                close = 'CLOSE,' + id + "," + str(lots)

            if bar_ago > 15 and profit == 0:
                close = 'CLOSE,' + id + "," + str(lots)

            orders = orders.iloc[:-1]

    else:
        p = df[CROSS + "CLOSE"].iloc[-1]
        r = avg(df_4hour, CROSS, window=avg_4h)

        action = rsi_info(df, CROSS, period=period_1h, thre_buy=thre_buy, thre_sell=thre_sell)
        if r != action:
            action = None
        TP = conf['TP']
        SL = conf['SL']
        if action == "SELL":
            trigger = p - in_pips(25, CROSS)
            p = trigger
            tp = p - in_pips(TP, CROSS)
            sl = p + in_pips(SL, CROSS)
            last_pos = action

        if action == "BUY":
            trigger = p + in_pips(25, CROSS)
            p = trigger
            tp = p + in_pips(TP, CROSS)
            sl = p - in_pips(SL, CROSS)
            last_pos = action

    if tp is None:
        action = None
    return trigger, tp, sl, action, close
