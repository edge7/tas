from flask import Blueprint, jsonify
from flask import current_app as app

rest_api = Blueprint('rest_api', __name__)


def get_strategy():
    return app.config["Strategy"]


def get_json_with_all_info(cross, strat_obj):
    to_return = {}
    to_return['Strumento'] = cross
    close = strat_obj.get_last_close()
    close = round(close, 4)
    to_return['LastClose'] = close
    to_return['MACD'] = strat_obj.get_last_signals_macd()
    to_return['BullishTrendLines'] = strat_obj.get_trend_line()
    to_return['BullishLines'] = strat_obj.get_lines()
    to_return['BearishTrendLines'] = strat_obj.get_trend_line(bearish=True)
    to_return['BearishLines'] = strat_obj.get_lines(bearish=True)
    to_return['bullishCandles'] = strat_obj.get_bullish_candles()
    to_return['bearishCandles'] = strat_obj.get_bearish_candles()
    to_return['distAVG50'] = strat_obj.get_avg(window=50)
    to_return['distAVG100'] = strat_obj.get_avg(window=100)
    return to_return


@rest_api.route("/get_last_close")
def get_last_close():
    to_return = {}
    for cross, strat_obj in app.config['Strategies'].items():
        close = strat_obj.get_last_close()
        close = round(close, 4)
        to_return[cross] = close
    return jsonify(to_return)


@rest_api.route("/get_last_macd_orders")
def get_last_macds():
    to_return = {}
    for cross, strat_obj in app.config['Strategies'].items():
        close = strat_obj.get_last_signals_macd()
        to_return[cross] = close
    return jsonify(to_return)


@rest_api.route("/get_crosses")
def get_crosses():
    to_return = []
    for cross, _ in app.config['Strategies'].items():
        to_return.append(cross)
    return jsonify(to_return)


@rest_api.route("/get_trendlines")
def get_trendlines():
    to_return = {}
    for cross, strat_obj in app.config['Strategies'].items():
        close = strat_obj.get_trend_line()
        close = round(close, 4)
        to_return[cross] = close
    return jsonify(to_return)


@rest_api.route("/get_lines")
def get_lines():
    to_return = {}
    for cross, strat_obj in app.config['Strategies'].items():
        close = strat_obj.get_lines()
        close = round(close, 4)
        to_return[cross] = close
    return jsonify(to_return)


@rest_api.route("/get_bullish_candles")
def get_bullish():
    to_return = {}
    for cross, strat_obj in app.config['Strategies'].items():
        close = strat_obj.get_bullish_candles()
        close = round(close, 4)
        to_return[cross] = close
    return jsonify(to_return)


@rest_api.route("/get_bearish_candles")
def get_bearish():
    to_return = {}
    for cross, strat_obj in app.config['Strategies'].items():
        close = strat_obj.get_bearish_candles()
        close = round(close, 4)
        to_return[cross] = close
    return jsonify(to_return)


@rest_api.route("/return_all")
def return_all():
    to_return = []
    for cross, strat_obj in app.config['Strategies'].items():
        res = get_json_with_all_info(cross, strat_obj)
        to_return.append(res)
    return jsonify(to_return)
