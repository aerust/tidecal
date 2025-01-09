from tidecal.calday import CalDay
from tidecal.dataparser import NOAADataParser

import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    data_file = "data/data_example.txt"
    days = NOAADataParser.parse(data_file)
    days = days[0:3]

    for i in range(len(days)):
        if i == 0:
            print(f"Skipping day {days[i].date} since it has no previous day")
        elif i == len(days) - 1:
            print(f"Skipping day {days[i].date} since it has no next day")
        else:
            curves = CalDay.get_curves(days[i], days[i-1], days[i+1])

            for (x, y) in curves:
                plt.plot(x, y)

            # Plot the graph
            plt.xticks(np.arange(0, 24, 3))
            plt.xlabel('hours')
            plt.ylabel('feet')
            plt.title(days[i].date)
            plt.grid(True)
            plt.show()
