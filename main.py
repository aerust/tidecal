from model.calday import CalDay
from model.dataparser import DataParser, NOAADataParser

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import calendar

if __name__ == '__main__':
    data_file = "example/data_example.txt"
    months = DataParser.group_by_month(NOAADataParser.parse(data_file))

    for month in months.keys():
        days = months[month]
        file_name = f"data/{calendar.month_name[month]}.pdf"
        with PdfPages(file_name) as pdf:
            for i in range(len(days)):
                if i == 0:
                    print(f"Skipping day {days[i].date} since it has no previous day")
                elif i == len(days) - 1:
                    print(f"Skipping day {days[i].date} since it has no next day")
                else:
                    curves = CalDay.get_curves(days[i], days[i-1], days[i+1])

                    plt.figure()
                    for (x, y) in curves:
                        plt.plot(x, y)

                    # Plot the graph
                    plt.xticks(np.arange(0, 24, 3))
                    plt.xlabel('hours')
                    plt.ylabel('feet')
                    plt.title(days[i].date)
                    plt.grid(True)
                    pdf.savefig()
