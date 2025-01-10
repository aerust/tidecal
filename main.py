from model.calyear import CalYear
from model.dataparser import TidePredictionParser, NOAADataParser, TimeAndDateMoonPhaseParser

MODES = ["MONTH", "YEAR"]
MODE = MODES[1]

if __name__ == '__main__':
    tide_data_file = "example/data_example.txt"

    if MODE == "MONTH":
        months = TidePredictionParser.get_months(NOAADataParser.parse(tide_data_file))
        for i in range(12):
            month = months[i]
            prev_month = months[i-1] if i > 0 else None
            next_month = months[i+1] if i < 11 else None
            month.plot(f"data/{month.name}.pdf", prev_month, next_month)
    else:
        moon_data_file = "example/moon_phases_san_juan_island_2025.csv"
        moon_phases = TimeAndDateMoonPhaseParser(2025).parse(moon_data_file)

        months = TidePredictionParser.get_months(NOAADataParser.parse(tide_data_file), moon_phases)
        year = CalYear(months)
        year.plot("data/2025.pdf")
