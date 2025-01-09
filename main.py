from model.calmonth import CalMonth
from model.dataparser import DataParser, NOAADataParser

if __name__ == '__main__':
    data_file = "example/data_example.txt"
    months = DataParser.group_by_month(NOAADataParser.parse(data_file))

    for i in range(12):
        days = months[i+1]
        month = CalMonth(i+1, days)
        month.plot(f"data/{month.name}.pdf")
