from model.calday import CalDay

import calendar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

class CalMonth:
    def __init__(self, number, days):
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

    def __get_curves(self, day, prev_month = None, next_month = None):
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
                        curves = self.__get_curves(day, prev_month, next_month)
                        for (x, y) in curves:
                            ax.plot(x, y, 'tab:blue')

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
