from model.calday import CalDay

import calendar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

class CalYear:
    def __init__(self, months):
        self.year = 2025
        month_map = {}
        for i in range(1, 13):
            month_map[i] = months[i-1]

        self.months = month_map

    def plot(self, filename):
        with PdfPages(filename) as pdf:
            fig = plt.figure()
            gs = fig.add_gridspec(12, 5, hspace=0, wspace=0)
            moon_phase_tuples = gs.subplots(sharex='col', sharey='row')
            fig.suptitle(f"{self.year}")
            for i in range(12):
                month = self.months[i+1]
                prev_month = self.months[i] if i > 0 else None
                next_month = self.months[i+2] if i < 11 else None

                days_by_moon_phase = month.get_days_by_moon_phase()
                phase_change_days = list(month.moon_phases.keys())
                for j in range(len(phase_change_days)):
                    ax = moon_phase_tuples[i][j]
                    phase_change_day = phase_change_days[j]
                    days = days_by_moon_phase[phase_change_day]
                    for day in days:
                        curves = month.get_curves(day, prev_month, next_month)
                        for (x, y) in curves:
                            ax.plot(x, y, 'tab:blue')

            for ax in fig.get_axes():
                ax.label_outer()

            pdf.savefig()
