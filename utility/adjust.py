from datetime import timedelta
import pandas as pd
import numpy as np

def adjust_data(df, CROSS, adjust_time=0):
    to_keep = ["TIME", CROSS + "CLOSE", CROSS + "OPEN", CROSS + "HIGH", CROSS + "LOW"]
    df = df[to_keep]
    df["TIME"] = df["TIME"].apply(lambda x: x - timedelta(hours=adjust_time))

    res = df[df["TIME"].apply(lambda x: x.hour) == 1].index[0]
    df_1 = df.iloc[res:].reset_index(drop=True)

    accumulate_time = []
    accumulate_close = []
    accumulate_open = []
    accumulate_high = []
    accumulate_low = []

    emit_time = []
    emit_close = []
    emit_open = []
    emit_high = []
    emit_low = []

    def is_last(h, g):
        for x in g:
            if h == x[-1]:
                return True
        return False

    groups = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16], [17, 18, 19, 20], [21, 22, 23, 0]]
    for index, row in df_1.iterrows():
        hour = row["TIME"].hour

        if is_last(hour, groups):
            if accumulate_close:
                accumulate_time.append(row["TIME"])
                accumulate_low.append(row[CROSS + "LOW"])
                accumulate_high.append(row[CROSS + "HIGH"])
                accumulate_close.append(row[CROSS + "CLOSE"])
                accumulate_open.append(row[CROSS + "OPEN"])

                emit_close.append(accumulate_close[-1])
                emit_high.append(max(accumulate_high))
                emit_low.append(min(accumulate_low))
                emit_time.append(max(accumulate_time))
                emit_open.append(accumulate_open[-1])
                if len(accumulate_low) != 4:
                    pass

                accumulate_time = []
                accumulate_close = []
                accumulate_open = []
                accumulate_high = []
                accumulate_low = []

            else:
                pass


        else:
            accumulate_time.append(row["TIME"])
            accumulate_low.append(row[CROSS + "LOW"])
            accumulate_high.append(row[CROSS + "HIGH"])
            accumulate_close.append(row[CROSS + "CLOSE"])
            accumulate_open.append(row[CROSS + "OPEN"])

    to_return = pd.DataFrame(
        {"TIME": emit_time, CROSS + "OPEN": emit_open, CROSS + "CLOSE": emit_close, CROSS + "HIGH": emit_high,
         CROSS + "LOW": emit_low})

    to_return[CROSS + "BODY"] = to_return[CROSS + "CLOSE"] - to_return[CROSS + "OPEN"]
    to_return[CROSS + "HIGHINPIPS"] = np.where(to_return[CROSS + "BODY"] >= 0,
                                               to_return[CROSS + "HIGH"] - to_return[CROSS + "CLOSE"],
                                               to_return[CROSS + "HIGH"] - to_return[CROSS + "OPEN"])
    to_return[CROSS + "LOWINPIPS"] = np.where(to_return[CROSS + "BODY"] >= 0,
                                               to_return[CROSS + "OPEN"] - to_return[CROSS + "LOW"],
                                               to_return[CROSS + "CLOSE"] - to_return[CROSS + "LOW"])
    return to_return

def adjust_data_daily(df, CROSS, adjust_time=0):
    to_keep = ["TIME", CROSS + "CLOSE", CROSS + "OPEN", CROSS + "HIGH", CROSS + "LOW"]
    df = df[to_keep]
    df["TIME"] = df["TIME"].apply(lambda x: x - timedelta(hours=adjust_time))

    res = df[df["TIME"].apply(lambda x: x.hour) == 4].index[0]
    df_1 = df.iloc[res:].reset_index(drop=True)

    accumulate_time = []
    accumulate_close = []
    accumulate_open = []
    accumulate_high = []
    accumulate_low = []

    emit_time = []
    emit_close = []
    emit_open = []
    emit_high = []
    emit_low = []

    def is_last(h, g):
        for x in g:
            if h == x[-1]:
                return True
        return False

    groups = [[20]]
    for index, row in df_1.iterrows():
        hour = row["TIME"].hour

        if is_last(hour, groups):
            if accumulate_close:
                accumulate_time.append(row["TIME"])
                accumulate_low.append(row[CROSS + "LOW"])
                accumulate_high.append(row[CROSS + "HIGH"])
                accumulate_close.append(row[CROSS + "CLOSE"])
                accumulate_open.append(row[CROSS + "OPEN"])

                emit_close.append(accumulate_close[-1])
                emit_high.append(max(accumulate_high))
                emit_low.append(min(accumulate_low))
                emit_time.append(max(accumulate_time))
                emit_open.append(accumulate_open[-1])
                if len(accumulate_low) != 4:
                    pass

                accumulate_time = []
                accumulate_close = []
                accumulate_open = []
                accumulate_high = []
                accumulate_low = []

            else:
                pass


        else:
            accumulate_time.append(row["TIME"])
            accumulate_low.append(row[CROSS + "LOW"])
            accumulate_high.append(row[CROSS + "HIGH"])
            accumulate_close.append(row[CROSS + "CLOSE"])
            accumulate_open.append(row[CROSS + "OPEN"])

    to_return = pd.DataFrame(
        {"TIME": emit_time, CROSS + "OPEN": emit_open, CROSS + "CLOSE": emit_close, CROSS + "HIGH": emit_high,
         CROSS + "LOW": emit_low})

    to_return[CROSS + "BODY"] = to_return[CROSS + "CLOSE"] - to_return[CROSS + "OPEN"]
    to_return[CROSS + "HIGHINPIPS"] = np.where(to_return[CROSS + "BODY"] >= 0,
                                               to_return[CROSS + "HIGH"] - to_return[CROSS + "CLOSE"],
                                               to_return[CROSS + "HIGH"] - to_return[CROSS + "OPEN"])
    to_return[CROSS + "LOWINPIPS"] = np.where(to_return[CROSS + "BODY"] >= 0,
                                               to_return[CROSS + "OPEN"] - to_return[CROSS + "LOW"],
                                               to_return[CROSS + "CLOSE"] - to_return[CROSS + "LOW"])
    return to_return
