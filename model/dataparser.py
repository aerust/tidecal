from model.tide import Tide, TideType
from model.calday import CalDay
from model.calmonth import CalMonth

import re
from datetime import datetime
from zoneinfo import ZoneInfo

class TidePredictionParser:
    @staticmethod
    def parse(file_path):
        pass

    @staticmethod
    def get_months(days):
        days_grouped = {}
        for day in days:
            month = day.date.month
            group = days_grouped.get(month)
            if group is None:
                days_grouped[month] = [day]
            else:
                days_grouped[month] = group + [day]

        months = []
        for i in range(12):
            days = days_grouped[i + 1]
            months = months + [CalMonth(i + 1, days)]

        return months

class NOAADataParser(TidePredictionParser):
    @staticmethod
    def parse(file_path, moon_data = None):
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
