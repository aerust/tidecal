from datetime import timedelta

class CalDay:
    """Calendar Day"""
    def __init__(self, tides, previous = None):
        date_set = set([tide.date() for tide in tides])
        if len(date_set) != 1:
            raise Exception("Invalid tide list", tides)

        self.date = date_set.pop()
        # TODO: this should be ordered
        self.tides = tides
        self.prev_date = self.date - timedelta(days=1)

    def __repr__(self):
        return f"Date: {self.date}, tides: {self.tides}, has previous: {self.previous is not None}"
