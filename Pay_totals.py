from loguru import logger
import tabula.io as tb
import pandas as pd
import re
import os

DIRECTORY = r'C:\users\justi\appdata\local\programs\python\python310\FinanceScripts\2022 Paystubs\\'
PATH = r'C:\users\justi\appdata\local\programs\python\python310\FinanceScripts\2022 Paystubs\\'
AREA = (0, 0, 612, 792)
KAT_COLS = [210, 288]
JUSTIN_COLS = [300, 390, 440, 475, 515, 590]

JUSTIN_TOTAL = 0.0
KAT_TOTAL = 0.0
MEDICARE = 0.0
MEDICARE_KAT = 0.0
HSA_EE = 0.0
FLEX_DEP = 0.0
FIT = 0.0
FIT_KAT = 0.0
SIT = 0.0
SIT_KAT = 0.0
CITY_TAX = 0.0
CITY_TAX_KAT = 0.0
SSN_TAX = 0.0
STD = 0.0
OPERS = 0.0
DEF_COMP = 0.0
_401k = 0.0
FIFTH_THIRD_DEPOSIT = 0.0
SCHWAB_DEPOSIT = 0.0
FIFTH_THIRD_DEPOSIT_KAT = 0.0
SCHWAB_DEPOSIT_KAT = 0.0
HEALTH_INS = 0.0

def clean_data(string):
    try:
        filter_object = filter(str.isdigit, string)
        new_string = "".join(filter_object)
        new_string = float(new_string)/100
        return new_string
    except TypeError as t:
        logger.info(t)
    except ValueError as v:
        logger.info(v)
    except KeyError:
        return 0.0


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
        self.id = 'Justin'
        self.pay_data = load_pdf_file(self.file, JUSTIN_COLS)
        self.pay_data_dict = {}


    def add_data(self):
        for row in range(5, 21):
            key = self.pay_data[0].loc[row, 1]
            value = clean_data(self.pay_data[0].loc[row, 2])
            self.pay_data_dict[key] = value
        for row in range(20, 24):
            key = self.pay_data[0].loc[row, 1]
            value = clean_data(self.pay_data[0].loc[row, 5])
            self.pay_data_dict[key] = value


class Kat_Paycheck(Paycheck):
    def __init__(self, file):
        super().__init__(file)
        self.id = 'Kat'
        self.pay_data = load_pdf_file(self.file, KAT_COLS)
        self.pay_data_dict = {}

    def add_data(self):
        for row in range(18, 31):
            key = self.pay_data[0].loc[row, 0]
            value = clean_data(self.pay_data[0].loc[row, 1])
            self.pay_data_dict[key] = value


paycheck_list = []
files = [file for file in os.listdir(DIRECTORY) if os.path.isfile(os.path.join(DIRECTORY, file))]
for file in files:
    print(file[:3])
    if file[:3] == 'Cit':
        paycheck = Justin_Paycheck(file)
        paycheck.add_data()
        print(paycheck.pay_data_dict)
        paycheck_list.append(paycheck)
    if file[:3] == 'Pay':
        paycheck = Kat_Paycheck(file)
        paycheck.add_data()
        print(paycheck.pay_data_dict)
        paycheck_list.append(paycheck)


print(paycheck_list)


# TOTAL FOR JUSTIN PAYCHECKS
for check in paycheck_list:
    if check.id == 'Justin':
        MEDICARE += check.pay_data_dict['MEDICARE']
        FIT += check.pay_data_dict['FIT']
        SIT += check.pay_data_dict['SIT']
        CITY_TAX += check.pay_data_dict['DELAWARE']
        DEF_COMP += check.pay_data_dict['DEF COMP']
        OPERS += check.pay_data_dict['OPERS']
        HSA_EE += check.pay_data_dict['HSA EE']
        FLEX_DEP += check.pay_data_dict['FLEX DEP']
        HEALTH_INS += check.pay_data_dict['HEALTH']
        HEALTH_INS += check.pay_data_dict['DENTAL']
        try:
            HEALTH_INS += check.pay_data_dict['VISION']
        except KeyError as e:
            logger.info(e)
        FIFTH_THIRD_DEPOSIT += check.pay_data_dict['FIFTH THIRD BANK']
        SCHWAB_DEPOSIT += check.pay_data_dict['JPMORGAN CHASE']
        JUSTIN_TOTAL = (
            MEDICARE +
            FIT +
            SIT +
            CITY_TAX +
            DEF_COMP +
            OPERS +
            HSA_EE +
            FLEX_DEP +
            HEALTH_INS +
            FIFTH_THIRD_DEPOSIT +
            SCHWAB_DEPOSIT
        )
    if check.id == 'Kat':
        MEDICARE_KAT += check.pay_data_dict['Medicare Tax']
        FIT_KAT += check.pay_data_dict['Federal Income Tax']
        SIT_KAT += check.pay_data_dict['OH State Income Tax']
        CITY_TAX_KAT += check.pay_data_dict['Columbus Income Tax']
        SSN_TAX += check.pay_data_dict['Social Security Tax']
        STD += check.pay_data_dict['Std Plan Aftx']
        _401k += check.pay_data_dict['401K Pre-Tax']
        FIFTH_THIRD_DEPOSIT_KAT += check.pay_data_dict['Checking 3']
        SCHWAB_DEPOSIT_KAT += check.pay_data_dict['Checking 1']
        KAT_TOTAL = (
            MEDICARE_KAT +
            FIT_KAT +
            SIT_KAT +
            CITY_TAX_KAT +
            SSN_TAX +
            STD +
            _401k +
            FIFTH_THIRD_DEPOSIT_KAT +
            SCHWAB_DEPOSIT_KAT
        )


print(f'Justin Pay total = {JUSTIN_TOTAL}')
print(f'Kat Pay total = {KAT_TOTAL}')
print(f'Fifth Third Deposit total = {FIFTH_THIRD_DEPOSIT + FIFTH_THIRD_DEPOSIT_KAT}')
print(f'Schwab Deposit total = {SCHWAB_DEPOSIT + SCHWAB_DEPOSIT_KAT}')
print(f'HSA Deposit total = {HSA_EE}')
print(f'Flex Spending Deposit total = {FLEX_DEP}')
print(f'OPERS total = {OPERS}')
print(f'457b total = {DEF_COMP}')
print(f'401k total = {_401k}')
print(f'Medicare total = {MEDICARE + MEDICARE_KAT}')
print(f'Fed Tax total = {FIT + FIT_KAT}')
print(f'State Tax total = {SIT + SIT_KAT}')
print(f'City Tax total = {CITY_TAX + CITY_TAX_KAT}')
print(f'Social Security Tax total = {SSN_TAX}')
print(f'Short Term Disability total = {STD}')
print(f'Health Insurance total = {HEALTH_INS}')



