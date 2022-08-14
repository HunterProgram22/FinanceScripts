from loguru import logger
import tabula as tb
import pandas as pd
import re
import os

DIRECTORY = r'C:\users\jkudela\appdata\local\programs\python\python310\Finance\FinanceScripts\2022 Paystubs\\'
PATH = r'C:\users\jkudela\appdata\local\programs\python\python310\Finance\FinanceScripts\2022 Paystubs\\'
AREA = (0, 0, 612, 792)
KAT_COLS = [150, 210, 288]
JUSTIN_COLS = [300, 390, 440, 475, 515, 590]

def clean_data(string):
    try:
        filter_object = filter(str.isdigit, string)
        new_string = "".join(filter_object)
        new_string = float(new_string)/100
        return new_string
    except TypeError as e:
        pass
        # logger.info(e)


def load_pdf_file(file: str, columns: tuple):
    df = tb.read_pdf(
        file,
        area=(0, 0, 612, 792),
        columns=columns,
        stream=True,
        guess=True,
        pages='1',
        pandas_options={'header': None}
    )
    return df


class Paycheck(object):
    def __init__(self, file):
        self.file = PATH + file


class Justin_Paycheck(Paycheck):
    def __init__(self, file):
        super().__init__(file)
        self.pay_data = load_pdf_file(self.file, JUSTIN_COLS)


    def print_data(self):
        for row in range(5, 21):
            key = self.pay_data[0].loc[row, 1]
            value = clean_data(self.pay_data[0].loc[row, 2])
            print(f"{key} is: {value}")
        for row in range(21, 23):
            key = self.pay_data[0].loc[row, 1]
            value = clean_data(self.pay_data[0].loc[row, 5])
            print(f"{key} is: {value}")


paycheck_list = []
files = [file for file in os.listdir(DIRECTORY) if os.path.isfile(os.path.join(DIRECTORY, file))]
for file in files:
    print(file[:3])
    if file[:3] == 'Cit':
        paycheck = Justin_Paycheck(file)
        paycheck.print_data()
        paycheck_list.append(paycheck)
    # if file[:3] == 'Pay':
    #     df = tb.read_pdf(PATH + file, area=(0,0 , 612, 792), columns=KAT_COLS, stream=True, guess=True, pages='1', pandas_options={'header': None})
    #     print(df)

print(paycheck_list)


