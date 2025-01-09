from enum import Enum
import numpy as np

TideType = Enum('TideType', [('High', 1), ('Low', 2)])

class Tide:
    """Tide model"""
    def __init__(self, datetime, prediction_ft, prediction_cm, tide_type, moon_phase = None):
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

    @staticmethod
    def get_curve(date, tide_1, tide_2):
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
        amplitude = np.abs((tide_2.prediction_ft - tide_1.prediction_ft) / 2)
        frequency = np.pi / half_period
        phase_shift = hour_2 if datetime_2.date() == date else 24 + hour_2
        vertical_shift = np.abs((tide_2.prediction_ft + tide_1.prediction_ft) / 2)
        flip = 1 if tide_2.tide_type == TideType.High else -1

        # Calculate the transformed cosine values
        y = flip * amplitude * np.cos(frequency * (x - phase_shift)) + vertical_shift

        return x, y
