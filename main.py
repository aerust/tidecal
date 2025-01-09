from tidecal.tide import Tide, TideType
from tidecal.calDay import CalDay

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import re
from datetime import datetime
from zoneinfo import ZoneInfo

def line_to_array(input_line):
    cols = re.sub(r'(\t)\1+', r'\1', input_line).split('\t')
    date = cols[0]
    datetime_var = datetime.strptime(f"{date} {cols[2]}", '%Y/%m/%d %H:%M')
    # TODO: correctly assign PST vs PDT
    datetime_var = datetime_var.replace(tzinfo=ZoneInfo("America/Los_Angeles"))
    pred_ft = cols[3]
    pred_cm = cols[4]
    tide_type = cols[5]
    return [datetime_var.date(), datetime_var, pred_ft, pred_cm, tide_type]

def model_tide(date, tide_1, tide_2):
    datetime_1 = tide_1.datetime
    datetime_2 = tide_2.datetime
    half_period = (datetime_2 - datetime_1).total_seconds() / 3600

    hour_1 = datetime_1.time().hour + float(datetime_1.time().minute) / 60
    hour_2 = datetime_2.time().hour + float(datetime_2.time().minute) / 60

    if datetime_1.date() == datetime_2.date():
        range_start = hour_1
        range_end = hour_2
    elif datetime_1.date() == date:
        range_start = hour_1
        range_end = 24
    else:
        range_start = 0
        range_end = hour_2

    x = np.linspace(range_start, range_end, 1000)

    # Define the transformation parameters
    amplitude = np.abs((tide_2.prediction_ft - tide_1.prediction_ft)/2)
    frequency = np.pi / half_period
    phase_shift = hour_2 if tide_2.tide_type == TideType.High else hour_1 - 24
    vertical_shift = np.abs((tide_2.prediction_ft + tide_1.prediction_ft)/2)

    # Calculate the transformed cosine values
    y = amplitude * np.cos(frequency * (x - phase_shift)) + vertical_shift

    return x, y

"""
Plot Day
"""
def plot_day(day, prev_day, next_day):
    tides_in_day = len(day.tides)
    # for i in range(tides_in_day + 1):
    #     if i == 0:
    #         (x,y) = model_tide(day.date, prev_day.tides[-1], day.tides[i])
    #     elif i == tides_in_day:
    #         (x,y) = model_tide(day.date, day.tides[i-1], next_day.tides[0])
    #     else:
    #         (x,y) = model_tide(day.date, day.tides[i-1], day.tides[i])

    i = 1
    (x, y) = model_tide(day.date, day.tides[i - 1], day.tides[i])
    print(day.tides[i - 1])
    print(day.tides[i])
    plt.plot(x, y)

    # Plot the graph
    plt.xlabel('hours')
    plt.ylabel('feet')
    plt.title('Transformed Cosine Function')
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    data = """Date 		Day	Time	Pred(Ft)	Pred(cm)	High/Low
2025/01/01	Wed	07:47	8.89		271			H
2025/01/01	Wed	12:33	7.46		227			L
2025/01/01	Wed	15:00	7.58		231			H
2025/01/01	Wed	23:43	-2.01		-61			L
2025/01/02	Thu	08:16	8.83		269			H
2025/01/02	Thu	13:22	6.97		212			L
2025/01/02	Thu	16:02	7.13		217			H
2025/01/03	Fri	00:23	-1.58		-48			L
2025/01/03	Fri	08:44	8.75		267			H
2025/01/03	Fri	14:23	6.21		189			L
2025/01/03	Fri	17:17	6.46		197			H"""

    lines = data.splitlines()[1:]
    tides_grouped = {}
    for line in lines:
        cols = re.sub(r'(\t)\1+', r'\1', line).split('\t')
        date = cols[0]
        datetime = datetime.strptime(f"{date} {cols[2]}", '%Y/%m/%d %H:%M')
        # TODO: correctly assign PST vs PD
        datetime = datetime.replace(tzinfo=ZoneInfo("America/Los_Angeles"))
        prediction_ft = cols[3]
        prediction_cm = cols[4]
        tide_type = TideType.High if cols[5] == 'H' else TideType.Low
        tide = Tide(datetime, prediction_ft, prediction_cm, tide_type)

        group = tides_grouped.get(date)
        if group is None:
            tides_grouped[date] = [tide]
        else:
            tides_grouped[date] = group + [tide]

    days = []
    for date in tides_grouped.keys():
        cal_day = CalDay(tides_grouped[date])
        days.append(cal_day)

    # data = np.array([line_to_array(input_line) for input_line in lines])
    #
    # df = pd.DataFrame({'Date': data[:, 0], 'Datetime': data[:, 1], 'Pred(ft)': data[:, 2], 'Pred(cm)': data[:, 3], 'High/Low': data[:, 4]})
    # df = df.astype({'Date': 'string', 'Datetime': 'datetime64[ns, America/Los_Angeles]', 'Pred(ft)': 'float', 'Pred(cm)': 'int', 'High/Low': 'string'})
    # print(df)
    # print(df.dtypes)

    for i in range(len(days)):
        if i == 0:
            print(f"Skipping day {days[i].date} since it has no previous day")
        elif i == len(days) - 1:
            print(f"Skipping day {days[i].date} since it has no next day")
        else:
            plot_day(days[i], days[i-1], days[i+1])
