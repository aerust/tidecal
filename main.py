from model.calmonth import CalMonth
from model.dataparser import TidePredictionParser, NOAADataParser

if __name__ == '__main__':
    data_file = "example/data_example.txt"
    months = TidePredictionParser.get_months(NOAADataParser.parse(data_file))

    for i in range(12):
        month = months[i]
        prev_month = months[i-1] if i > 0 else None
        next_month = months[i+1] if i < 11 else None
        month.plot(f"data/{month.name}.pdf", prev_month, next_month)
