import tabula as tb
import pandas as pd
import re

PATH = "C:\\Users\\Justin Kudela\\Desktop\\"

kat_file = PATH + 'TestCheck2.pdf'
justin_file = PATH + 'TestCheck.pdf'

def kat_paycheck(file):
    df = tb.read_pdf(file, area=(0,0 , 612, 792), columns=[150, 210, 288], stream=True, guess=True, pages='1', pandas_options={'header': None})

    gross_pay = df[0].loc[14, 2]
    federal_tax = df[0].loc[18, 2]
    social_security = df[0].loc[19, 2]
    medicare = df[0].loc[21, 2]
    ohio_tax = df[0].loc[22, 2]
    cbus_tax = df[0].loc[23, 2]
    short_term_disability = df[0].loc[26, 2]
    four_01k = df[0].loc[27, 2]
    net_pay = df[0].loc[28, 2]
    schwab_deposit = df[0].loc[29, 2]
    fifth_third_deposit = df[0].loc[30, 2]

    paycheck_items = (gross_pay, federal_tax, social_security, medicare, ohio_tax, cbus_tax, short_term_disability, four_01k, net_pay, schwab_deposit, fifth_third_deposit)

    return paycheck_items

def justin_paycheck(file):
    df = tb.read_pdf(file, area=(0,0 , 612, 792), columns=[390, 440, 475, 515, 590], stream=True, guess=True, pages='1', pandas_options={'header': None})

    gross_pay = df[0].loc[31, 3]
    federal_tax = df[0].loc[6, 1]
    medicare = df[0].loc[5, 1]
    ohio_tax = df[0].loc[7, 1]
    city_tax = df[0].loc[8, 1]
    four_57b = df[0].loc[12, 1]
    net_pay = df[0].loc[33, 3]
    schwab_deposit = df[0].loc[17, 4]
    fifth_third_deposit = df[0].loc[18, 4]

    paycheck_items = (gross_pay, federal_tax, medicare, ohio_tax, city_tax, four_57b, net_pay, schwab_deposit, fifth_third_deposit)

    return paycheck_items

def clean_data(string):
    filter_object = filter(str.isdigit, string)
    new_string = "".join(filter_object)
    new_string = float(new_string)/100
    return new_string

paycheck_items = kat_paycheck(kat_file)
kat_new_paycheck_items = map(clean_data, paycheck_items)

print(tuple(kat_new_paycheck_items))

paycheck_items = justin_paycheck(justin_file)
justin_new_paycheck_items = map(clean_data, paycheck_items)

print(tuple(justin_new_paycheck_items))
