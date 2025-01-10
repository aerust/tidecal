from model.moonphase import MoonPhase
from model.tide import Tide, TideType
from model.calday import CalDay
from model.calmonth import CalMonth

import csv
import re
from datetime import datetime
from zoneinfo import ZoneInfo

class MoonPhaseParser:
    def parse(self, file_path):
        pass

class TimeAndDateMoonPhaseParser(MoonPhaseParser):
    def __init__(self, year):
        self.year = year

    def __get_phase_from_row(self, phase, row):
        date = row[phase]
        time = row[phase + ' Time']

        if date == '':
            return None
        else:
            date_time = datetime.strptime(f"{self.year} {date} {time}", '%Y %b %d %H:%M')
            # TODO: correctly assign PST vs PDT
            date_time = date_time.replace(tzinfo=ZoneInfo("America/Los_Angeles"))

            return MoonPhase(date_time, MoonPhase.get_type(phase))

    def parse(self, file_path):
        with open(file_path, 'r') as file:
            moon_phases = []
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                # CSV Header from timanddate.com:
                # Lunation,New Moon,New Moon Time,First Quarter,First Quarter Time,Full Moon,Full Moon Time,Third Quarter,Third Quarter Time,Duration
                phases = ['New Moon', 'First Quarter', 'Full Moon', 'Third Quarter']
                moon_phases = moon_phases + [self.__get_phase_from_row(phase, row) for phase in phases]

        moon_phases = filter(None, moon_phases)
        month_map = {}
        for phase in moon_phases:
            group = month_map.get(phase.month_number)
            if group is None:
                month_map[phase.month_number] = [phase]
            else:
                month_map[phase.month_number] = group + [phase]

        for month in month_map.keys():
            month_map[month].sort()

        return month_map

class TidePredictionParser:
    @staticmethod
    def parse(file_path):
        pass

    @staticmethod
    def get_months(days, moon_phases = None):
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
            month_moon_phases = moon_phases[i + 1] if moon_phases is not None else None
            months = months + [CalMonth(i + 1, days, month_moon_phases)]

        return months

class NOAADataParser(TidePredictionParser):
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
