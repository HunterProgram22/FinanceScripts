import tabula as tb
import pandas as pd
import re

PATH = "C:\\Users\\Justin Kudela\\Desktop\\"

justin_file = PATH + 'TestCheck.pdf'

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

paycheck_items = justin_paycheck(justin_file)
new_paycheck_items = map(clean_data, paycheck_items)

print(tuple(new_paycheck_items))
