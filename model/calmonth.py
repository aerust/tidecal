from model.calday import CalDay

import calendar
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

class CalMonth:
    def __init__(self, number, days, moon_phases = None):
        if number < 1 or number > 12:
            raise Exception("Month number must be 1-12: ", number)

        self.number = number
        self.name = calendar.month_name[number]
        self.year = days[0].date.year
        days_map = {}
        for day in days:
            days_map[day.number] = day
        self.days = days_map
        self.length = len(self.days.keys())
        self.weeks = self.__group_days_by_week()
        self.weeks_count = len(self.weeks.keys())
        moon_phases_map = {}
        if moon_phases is not None:
            for moon_phase in moon_phases:
                moon_phases_map[moon_phase.datetime.day] = moon_phase
            self.moon_phases = moon_phases_map
        else:
            self.moon_phases = None

        self.days_gouped_by_moon_phase = None

    def __group_days_by_week(self):
        week_number = 0
        grouped_by_week = {}
        for i in range(self.length):
            day = self.days[i+1]
            if i == 0 or day.weekday_number == 0:
                # start a new week
                week_number = week_number + 1
                grouped_by_week[week_number] = [day]
            else:
                grouped_by_week[week_number] = grouped_by_week[week_number] + [day]

        return grouped_by_week

    def get_days_by_moon_phase(self):
        if self.moon_phases is None:
            raise Exception("Month.moon_phases must not be None")

        if self.days_gouped_by_moon_phase is not None:
            return self.days_gouped_by_moon_phase

        new_phase_days = list(self.moon_phases.keys())
        new_phase_days.sort()
        day_ranges_map = {}
        for i in range(len(new_phase_days)):
            new_phase_day = new_phase_days[i]
            if i < len(new_phase_days) - 1:
                day_ranges_map[new_phase_day] = range(new_phase_day, new_phase_days[i+1] - 1)
            else:
                day_ranges_map[new_phase_day] = range(new_phase_day, self.length)

        days_grouped = {}
        for new_phase_day in new_phase_days:
            day_range = day_ranges_map[new_phase_day]
            phase_days = []
            for day in day_range:
                phase_days = phase_days + [self.days[day]]
            days_grouped[new_phase_day] = phase_days

        self.days_gouped_by_moon_phase = days_grouped
        return self.days_gouped_by_moon_phase

    def get_curves(self, day, prev_month = None, next_month = None):
        day_number = day.number

        prev_day = self.days.get(day_number-1)
        if day_number == 1 and prev_month is not None:
            prev_day = prev_month.days[prev_month.length]

        next_day = self.days.get(day_number+1)
        if day_number == self.length and next_month is not None:
            next_day = next_month.days[1]

        return CalDay.get_curves(self.days[day_number], prev_day, next_day)

    def plot(self, filename, prev_month = None, next_month = None):
        # Fill out partial weeks with Nones, so each week is an array of length 7
        full_weeks = {}
        for i in range(self.weeks_count):
            week = self.weeks[i+1]
            week_length = len(week)
            if week_length < 7:
                pad = [None] * (7 - week_length)
                if week[0].number == 1:
                    full_weeks[i+1] = pad + week
                else:
                    full_weeks[i+1] = week + pad
            elif week_length == 7:
                full_weeks[i+1] = week
            else:
                raise Exception("Week had unexpected length")

        weeks = full_weeks
        weeks_count = len(weeks.keys())

        with PdfPages(filename) as pdf:
            fig = plt.figure()
            gs = fig.add_gridspec(weeks_count, 7, hspace=0, wspace=0)
            septuples = gs.subplots(sharex='col', sharey='row')
            fig.suptitle(f"{self.name} {self.year}")
            for i in range(weeks_count):
                for j in range(7):
                    ax = septuples[i][j]
                    day = weeks[i+1][j]
                    if day is not None:
                        curves = self.get_curves(day, prev_month, next_month)
                        for (x, y) in curves:
                            ax.plot(x, y, 'tab:blue')

                        moon_phase = self.moon_phases.get(day.number)
                        if moon_phase is not None:
                            x = np.linspace(0, 24, 1000)
                            y = np.linspace(15, 15, 1000)
                            ax.plot(x,y, 'tab:red', label=moon_phase.moon_phase_name)
                            ax.legend(loc="upper right", fontsize="x-small")

            for ax in fig.get_axes():
                ax.label_outer()

            pdf.savefig()

            # plt.figure()
            # for (x, y) in curves:
            #     plt.plot(x, y)
            #
            # # Plot the graph
            # plt.xticks(np.arange(0, 24, 3))
            # plt.xlabel('hours')
            # plt.ylabel('feet')
            # plt.title(days[i].date)
            # plt.grid(True)
            # pdf.savefig()
