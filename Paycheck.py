import tabula as tb
import pandas as pd
import re

PATH = "C:\\Users\\Justin Kudela\\Desktop\\"

kat_file = PATH + 'TestCheck2.pdf'
justin_file = PATH + 'TestCheck.pdf'

class Paycheck:
    def __init__(self, paycheck_items):
        self.gross_pay = paycheck_items['gross_pay']
        self.federal_tax = paycheck_items['federal_tax']
        self.social_security = paycheck_items['social_security']
        self.medicare = paycheck_items['medicare']
        self.ohio_tax = paycheck_items['ohio_tax']
        self.cbus_tax = paycheck_items['city_tax']
        self.short_term_disability = paycheck_items['short_term_disability']
        self.four_01k = paycheck_items['four_01k']
        self.four_57b = paycheck_items['four_57b']
        self.net_pay = paycheck_items['net_pay']
        self.schwab_deposit = paycheck_items['schwab_deposit']
        self.fifth_third_deposit = paycheck_items['fifth_third_deposit']


def kat_paycheck(file):
    df = tb.read_pdf(file, area=(0,0 , 612, 792), columns=[150, 210, 288], stream=True, guess=True, pages='1', pandas_options={'header': None})

    pay_dict = {
        "gross_pay": clean_data(df[0].loc[14, 2]),
        "federal_tax": clean_data(df[0].loc[18, 2]),
        "social_security": clean_data(df[0].loc[19, 2]),
        "medicare": clean_data(df[0].loc[21, 2]),
        "ohio_tax": clean_data(df[0].loc[22, 2]),
        "city_tax": clean_data(df[0].loc[23, 2]),
        "short_term_disability": clean_data(df[0].loc[26, 2]),
        "four_01k": clean_data(df[0].loc[27, 2]),
        "four_57b": 0.0,
        "net_pay": clean_data(df[0].loc[28, 2]),
        "schwab_deposit": clean_data(df[0].loc[29, 2]),
        "fifth_third_deposit": clean_data(df[0].loc[30, 2])
    }
    return pay_dict

def justin_paycheck(file):
    df = tb.read_pdf(file, area=(0,0 , 612, 792), columns=[390, 440, 475, 515, 590], stream=True, guess=True, pages='1', pandas_options={'header': None})

    pay_dict = {
        "gross_pay": clean_data(df[0].loc[31, 3]),
        "federal_tax": clean_data(df[0].loc[6, 1]),
        "social_security": 0.0,
        "medicare": clean_data(df[0].loc[5, 1]),
        "ohio_tax": clean_data(df[0].loc[7, 1]),
        "city_tax": clean_data(df[0].loc[8, 1]),
        "short_term_disability": 0.0,
        "four_01k": 0.0,
        "four_57b": clean_data(df[0].loc[12, 1]),
        "net_pay": clean_data(df[0].loc[33, 3]),
        "schwab_deposit": clean_data(df[0].loc[17, 4]),
        "fifth_third_deposit": clean_data(df[0].loc[18, 4])
    }
    return pay_dict

def clean_data(string):
    filter_object = filter(str.isdigit, string)
    new_string = "".join(filter_object)
    new_string = float(new_string)/100
    return new_string

paycheck_items = kat_paycheck(kat_file)
test_pay = Paycheck(paycheck_items)

justin_items = justin_paycheck(justin_file)
test_pay_2 = Paycheck(justin_items)
