import datetime
from enum import Enum

TideType = Enum('TideType', [('High', 1), ('Low', 2)])

class Tide:
    """Tide model"""
    def __init__(self, datetime, prediction_ft, prediction_cm, tide_type, moon_phase = None):
        # self.date = date
        # self.day = day
        # self.time = time
        self.datetime = datetime
        self.prediction_ft = float(prediction_ft)
        self.prediction_cm = int(prediction_cm)
        self.tide_type = tide_type
        self.moon_phase = moon_phase

    def __repr__(self):
        return f"Datetime: {self.datetime}, Pred(ft): {self.prediction_ft}, Pred(cm): {self.prediction_cm}, {self.tide_type}"

    def date(self):
        return self.datetime.date()

    def time(self):
        return self.datetime.time()
