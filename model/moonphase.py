from enum import Enum

MoonPhaseType = Enum('MoonPhaseType', [('NewMoon', 1), ('FirstQuarter', 2), ('FullMoon', 3), ('ThirdQuarter', 4)])

class MoonPhase:
    def __init__(self, datetime, moon_phase_type):
        self.datetime = datetime
        self.month_number = self.datetime.month
        self.moon_phase_type = moon_phase_type

    def __lt__(self, other):
        return self.datetime < other.datetime

    def __repr__(self):
        return f"Datetime: {self.datetime}, Phase: {self.moon_phase_type}"

    @staticmethod
    def get_type(type_string):
        if type_string == 'New Moon':
            return MoonPhaseType.NewMoon
        elif type_string == 'First Quarter':
            return MoonPhaseType.FirstQuarter
        elif type_string == 'Full Moon':
            return MoonPhaseType.FullMoon
        elif type_string == 'Third Quarter':
            return MoonPhaseType.ThirdQuarter
        else:
            raise Exception("Invalid phase string: ", type_string)

