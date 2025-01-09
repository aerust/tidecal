from model.tide import Tide

class CalDay:
    """Calendar Day"""
    def __init__(self, tides, previous = None):
        date_set = set([tide.date() for tide in tides])
        if len(date_set) != 1:
            raise Exception("Invalid tide list", tides)

        self.date = date_set.pop()
        self.number = self.date.day
        # Get the day of the week as an integer (0 = Monday, 6 = Sunday)
        self.weekday_number = self.date.weekday()
        # TODO: this should be ordered
        self.tides = tides

    def __repr__(self):
        return f"Date: {self.date}, tides: {self.tides}"

    @staticmethod
    def get_curves(day, prev_day, next_day):
        tides_in_day = len(day.tides)
        curves = []
        for i in range(tides_in_day + 1):
            if (i != 0 or prev_day is not None) and (i != tides_in_day or next_day is not None):
                if i == 0:
                    (x, y) = Tide.get_curve(day.date, prev_day.tides[-1], day.tides[i])
                elif i == tides_in_day:
                    (x, y) = Tide.get_curve(day.date, day.tides[i - 1], next_day.tides[0])
                else:
                    (x, y) = Tide.get_curve(day.date, day.tides[i - 1], day.tides[i])

                curves.append((x, y))

        return curves
