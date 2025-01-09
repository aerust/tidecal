from model.tide import Tide, TideType
from model.calday import CalDay

import re
from datetime import datetime
from zoneinfo import ZoneInfo

class DataParser:
    @staticmethod
    def parse(file_path):
        pass

class NOAADataParser(DataParser):
    @staticmethod
    def parse(file_path):
        file = open(file_path, "r")
        tides_grouped = {}
        for line in file:
            cols = re.sub(r'(\t)\1+', r'\1', line.strip()).split('\t')
            date = cols[0]
            date_time = datetime.strptime(f"{date} {cols[2]}", '%Y/%m/%d %H:%M')
            # TODO: correctly assign PST vs PDT
            date_time = date_time.replace(tzinfo=ZoneInfo("America/Los_Angeles"))
            prediction_ft = cols[3]
            prediction_cm = cols[4]
            tide_type = TideType.High if cols[5] == 'H' else TideType.Low
            tide = Tide(date_time, prediction_ft, prediction_cm, tide_type)

            group = tides_grouped.get(date)
            if group is None:
                tides_grouped[date] = [tide]
            else:
                tides_grouped[date] = group + [tide]

        days = []
        for date in tides_grouped.keys():
            cal_day = CalDay(tides_grouped[date])
            days.append(cal_day)

        return days
