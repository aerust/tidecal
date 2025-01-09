from tidecal.tide import Tide, TideType
from tidecal.calDay import CalDay

from datetime import datetime
from zoneinfo import ZoneInfo
import re

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

    print(days)
