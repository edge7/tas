from copy import deepcopy


class CandleStickInfo(object):
    def __init__(self, df, mi, CROSS):
        self.df = df
        self.SPINNING_THRES = 3
        self.MAR = 10
        self.spinning_tops = None
        self.mi = mi
        self.CROSS = CROSS

    def in_pips(self, param):
        if 'JPY' in self.CROSS or 'XAU' in self.CROSS or 'XAG' in self.CROSS:
            multiply = 100.0
        else:
            multiply = 10000.0
        return param / multiply

    def get_pips(self, body):
        if 'JPY' in self.CROSS or 'XAU' in self.CROSS or 'XAG' in self.CROSS:
            multiply = 100.0
        else:
            multiply = 10000.0
        return body * multiply

    def search_patterns(self):
        self.spinning_tops = self.search_spinning_top()
        self.marubozu = self.search_marubozu()
        self.hammer = self.search_hammer()
        self.hanging = self.search_hanging()
        self.inverted_hammer = self.search_inverted_hammer()
        self.shooting_start = self.search_shooting_star()
        self.bullish_engulfing = self.search_bullish_engulfing()

        self.bearish_engulfing = self.search_bearish_engulfing()

        self.tweezer_bottoms = self.search_tweez_bot()
        self.tweezer_tops = self.search_tweez_top()
        self.evening_star = self.search_evening_star()
        self.morning_star = self.search_moning_star()
        self.three_white = self.search_three_white()
        self.three_black = self.search_three_black()
        self.three_ins_up = self.search_3_up()
        self.three_ins_down = self.search_3_down()
        self.dragonfly = self.search_dragonfly_doji()
        self.gravestone = self.search_gravestone_doji()

    def search_spinning_top(self):
        last_body = abs(self.get_body(1))
        last_high = self.get_high(1)
        last_low = self.get_low(1)
        if last_body * self.SPINNING_THRES < last_high and last_body * self.SPINNING_THRES < last_low \
                and last_high / last_low < 1.8:
            return True
        return False

    def get_body(self, i):
        return self.df["BODY"].iloc[-1 * i]

    def get_high(self, i):
        return self.df["HIGHINPIPS"].iloc[-1 * i]

    def get_low(self, i):
        return self.df["LOWINPIPS"].iloc[-1 * i]

    def get_close(self, i):
        return self.df['CLOSE'].iloc[-1 * i]

    def get_open(self, i):
        return self.df['OPEN'].iloc[-1 * i]

    def search_marubozu(self):
        last_body = abs(self.get_body(1))
        if self.get_pips(abs(last_body)) < 13.0: return None
        last_high = self.get_high(1)
        last_low = self.get_low(1)
        if last_high * self.MAR < last_body and last_body > last_low * self.MAR:
            if self.get_body(1) > 0:
                return 'white'
            else:
                return 'black'
        return None

    def search_hammer(self):


        if not (self.get_close(1) < self.get_close(2) < self.get_close(3)) < self.get_close(4) < self.get_close(5):
            return False

        if not self.get_close(1) < self.get_close(6):
            return False

        last_body = abs(self.get_body(1))
        last_high = self.get_high(1)
        last_low = self.get_low(1)
        if last_low > 2.5 * abs(last_body) and last_low > 5 * last_high:
            return True

        return False

    def search_hanging(self):


        if not (self.get_close(1) > self.get_close(2) > self.get_close(3) > self.get_close(4)):
            return False

        if self.get_close(1) < self.get_close(5):
            return False

        last_body = abs(self.get_body(1))
        last_high = self.get_high(1)
        last_low = self.get_low(1)

        if last_low > 2.5 * abs(last_body) and last_low > 5 * last_high:
            return True

        return False

    def search_inverted_hammer(self):


        if not (self.get_close(1) < self.get_close(2) < self.get_close(3) < self.get_close(4)):
            return False

        last_body = abs(self.get_body(1))
        last_high = self.get_high(1)
        last_low = self.get_low(1)
        if last_high > 2.5 * abs(last_body) and last_high > 5 * last_low:
            return True

        return False

    def search_shooting_star(self):


        if not (self.get_close(1) > self.get_close(2) > self.get_close(3)):
            return False

        if self.get_close(1) < self.get_close(4):
            return False

        last_body = abs(self.get_body(1))
        last_high = self.get_high(1)
        last_low = self.get_low(1)
        if last_high > 2.5 * abs(last_body) and last_high > 5 * last_low:
            return True

        return False

    def search_bullish_engulfing(self):

        last_body = self.get_body(1)
        previous_body = self.get_body(2)
        pips_body = self.get_pips(abs(last_body))
        if pips_body > 12 and last_body > 0 > previous_body and abs(last_body) > abs(previous_body) * 1.5:
            return True

        return False

    def search_bearish_engulfing(self):
        is_bullish = True
        if not is_bullish:
            return False

        last_body = self.get_body(1)
        previous_body = self.get_body(2)
        pips_body = abs(self.get_pips(last_body))
        if pips_body > 12 and last_body < 0 < previous_body and abs(last_body) > abs(previous_body) * 1.5:
            return True

        return False

    def search_tweez_bot(self):

        last_body = self.get_body(1)
        previous_body = self.get_body(2)
        last_low = self.get_low(1)
        previous_low = self.get_low(2)
        if previous_body < 0 < last_body and (1.10 > last_low / previous_low > 0.90) and \
                (1.10 > abs(last_body / previous_body) > 0.90):
            return True
        return False

    def search_tweez_top(self):

        last_body = self.get_body(1)
        previous_body = self.get_body(2)
        last_high = self.get_high(1)
        previous_high = self.get_high(2)

        if previous_body > 0 > last_body and (1.10 > last_high / previous_high > 0.90) and \
                (1.10 > abs(last_body / previous_body) > 0.90):
            return True
        return False

    def search_evening_star(self):

        if self.get_close(3) < self.get_close(7):
            return False
        body_3 = self.get_body(3)
        if body_3 < 0: return False
        previous_body = self.get_body(2)
        last_body = self.get_body(1)
        if abs(previous_body) * 3 < abs(body_3) and abs(previous_body) * 3 < abs(last_body) \
                and last_body < 0 and self.get_close(1) < self.get_close(3) - body_3 * 0.55:
            return True
        return False

    def search_dragonfly_doji(self):
        close = self.get_close(1)
        close_ago = self.get_close(4)
        close_ago_ago = self.get_close(7)
        close_ago_ago_ago = self.get_close(13)
        if close < close_ago and close < close_ago_ago and close < close_ago_ago_ago:
            body = self.get_body(1)
            high = self.get_high(1)
            low = self.get_low(1)
            if abs(body) < self.in_pips(5) < low and high < self.in_pips(5) and low * 0.75 > high and self.get_pips(low) > 10:
                return True
        return False

    def search_gravestone_doji(self):
        close = self.get_close(1)
        close_ago = self.get_close(4)
        close_ago_ago = self.get_close(7)
        close_ago_ago_ago = self.get_close(13)
        if close > close_ago and close > close_ago_ago and close > close_ago_ago_ago:
            body = self.get_body(1)
            high = self.get_high(1)
            low = self.get_low(1)
            if abs(body) < self.in_pips(5) < high and low < self.in_pips(5) and high * 0.75 > low and self.get_pips(high) > 10:
                return True
        return False

    def search_moning_star(self):

        body_3 = self.get_body(3)
        if body_3 > 0: return False
        if self.get_close(3) > self.get_close(7) and self.get_close(3) > self.get_close(5):
            return False
        previous_body = self.get_body(2)
        last_body = self.get_body(1)
        if abs(last_body) > self.get_close(1) * 1.2 and abs(previous_body) * 3 < abs(body_3) and abs(
                previous_body) * 3 < abs(last_body) \
                and last_body > 0 and self.get_close(1) > self.get_close(3) - body_3 * 0.55:
            return True
        return False

    def search_three_white(self):

        last_body = self.get_body(1)
        previous_body = self.get_body(2)
        body_3 = self.get_body(3)
        if last_body < 0 or previous_body < 0 or body_3 < 0:
            return False
        if previous_body < body_3:
            return False
        previous_high = self.get_high(2)
        if previous_high * 5 > previous_body:
            return False
        if last_body >= previous_body and last_body / self.get_high(1) > 1.5 and last_body > self.get_low(1):
            return True
        return False

    def search_three_black(self):

        last_body = self.get_body(1)
        previous_body = self.get_body(2)
        body_3 = self.get_body(3)
        if last_body > 0 or previous_body > 0 or body_3 > 0:
            return False
        if abs(previous_body) < abs(body_3):
            return False
        previous_high = self.get_high(2)
        if previous_high * 5 > previous_body:
            return False
        if abs(last_body) >= abs(previous_body) and abs(last_body) / self.get_high(1) > 1.5 and abs(
                last_body) > self.get_low(1):
            #self.logger.info("Got 3 soldiers .. Sell this shit")
            return True
        return False

    def search_3_up(self):

        if self.get_close(3) < self.get_close(2) < self.get_close(1) \
                and self.get_body(2) > 0 \
                and self.get_body(1) > 0 \
                and self.get_body(3) < 0 and abs(self.get_body(2)) > abs(self.get_body(3)) * 0.6 \
                and self.get_close(1) > self.get_open(3) + self.get_high(3):

            return True

        return False

    def search_3_down(self):

        if self.get_close(3) > self.get_close(2) > self.get_close(1) \
                and self.get_body(2) < 0 \
                and self.get_body(1) < 0 \
                and self.get_body(3) > 0 and abs(self.get_body(2)) > abs(self.get_body(3)) * 0.6 \
                and self.get_close(1) < self.get_open(3) - self.get_low(3):
            return True


class MarketInfo(object):

    def __init__(self, df, CROSS):
        self.df = df
        self.short_trend = None
        self.long_trend = None
        self.medium_trend = None
        self.low_band_50 = None
        self.high_band_50 = None
        self.CROSS = CROSS

    def remove(self, df):
        for row in list(df.columns):
            df[row.replace(self.CROSS, '')] = df[row]
            del df[row]
        return df

    def get_body(self, i):
        return self.df[self.CROSS + "BODY"].iloc[-1 * i]

    def get_high(self, i):
        return self.df[self.CROSS + "HIGHINPIPS"].iloc[-1 * i]

    def get_low(self, i):
        return self.df[self.CROSS + "LOWINPIPS"].iloc[-1 * i]

    def get_close(self, i):
        return self.df[self.CROSS + 'CLOSE'].iloc[-1 * i]

    def get_open(self, i):
        return self.df[self.CROSS + 'OPEN'].iloc[-1 * i]

    def search_for_info(self):
        self.candle_info = CandleStickInfo(self.remove(deepcopy(self.df.tail(200))), self, self.CROSS)
        self.candle_info.search_patterns()
