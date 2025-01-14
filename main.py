from model.calyear import CalYear
from model.dataparser import TidePredictionParser, NOAADataParser, TimeAndDateMoonPhaseParser

MODES = ["MONTH", "YEAR"]
MODE = MODES[0]

if __name__ == '__main__':
    # TODO: finish debugging why PATH changes don't work
    # work-a-round:
    #  - replace 'latex' with '/Library/TeX/texbin/latex' in texmanager.py
    #  - replace 'kpsewhich' with '/Library/TeX/texbin/kpsewhich' in dviread.py
    #
    # import os
    # os.environ["PATH"] += os.pathsep + '/Library/TeX/texbin'
    # print(os.environ['PATH'])
    # import subprocess
    # command = ['/Library/TeX/texbin/latex', '-interaction=nonstopmode', '--halt-on-error', '--output-directory=data', 'example/example.tex']
    # env = os.environ.copy()
    # report = subprocess.check_output(command, env=env)
    # print(report)
    # command = ['/Library/TeX/texbin/kpsewhich', 'cmss17.tfm']
    # kwargs = {'encoding': 'utf-8', 'errors': 'surrogateescape'}
    # result = subprocess.run(command, **kwargs, env=env)
    # print(result)

    tide_data_file = "example/data_example.txt"
    moon_data_file = "example/moon_phases_san_juan_island_2025.csv"
    moon_phases = TimeAndDateMoonPhaseParser(2025).parse(moon_data_file)

    months = TidePredictionParser.get_months(NOAADataParser.parse(tide_data_file), moon_phases)
    if MODE == "MONTH":
        for i in range(12):
            month = months[i]
            prev_month = months[i-1] if i > 0 else None
            next_month = months[i+1] if i < 11 else None
            month.plot(f"data/{month.name}.pdf", prev_month, next_month)
    else:
        year = CalYear(months)
        year.plot("data/2025.pdf")
