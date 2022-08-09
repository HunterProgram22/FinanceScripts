import tabula as tb
import pandas as pd
import re
import os

DIRECTORY = r'C:\users\jkudela\appdata\local\programs\python\python310\Finance\FinanceScripts\2022 Paystubs\\'
PATH = r'C:\users\jkudela\appdata\local\programs\python\python310\Finance\FinanceScripts\2022 Paystubs\\'
AREA = (0, 0, 612, 792)
KAT_COLS = [150, 210, 288]
JUSTIN_COLS = [390, 440, 475, 515, 590]

paycheck_list = []
files = [file for file in os.listdir(DIRECTORY) if os.path.isfile(os.path.join(DIRECTORY, file))]
for file in files:
    print(file[:3])
    if file[:3] == 'Cit':
        df = tb.read_pdf(PATH + file, area=(0,0 , 612, 792), columns=JUSTIN_COLS, stream=True, guess=True, pages='1', pandas_options={'header': None})
        print(df)
    if file[:3] == 'Pay':
        df = tb.read_pdf(PATH + file, area=(0,0 , 612, 792), columns=KAT_COLS, stream=True, guess=True, pages='1', pandas_options={'header': None})
        print(df)
    paycheck_list.append(file)

print(paycheck_list)
