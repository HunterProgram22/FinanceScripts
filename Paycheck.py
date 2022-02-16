import tabula as tb
import pandas as pd
import re
import os
from loguru import logger

DIRECTORY = "C:\\Users\\Justin Kudela\\Desktop\\Paychecks"
PATH = "C:\\Users\\Justin Kudela\\Desktop\\Paychecks\\"



@logger.catch
class Paycheck:
    def __init__(self, paycheck_items):
        self.justin_gross_pay = paycheck_items['justin_gross_pay']
        self.kat_gross_pay = paycheck_items['kat_gross_pay']
        self.federal_tax = paycheck_items['federal_tax']
        self.social_security = paycheck_items['social_security']
        self.medicare = paycheck_items['medicare']
        self.ohio_tax = paycheck_items['ohio_tax']
        self.city_tax = paycheck_items['city_tax']
        self.short_term_disability = paycheck_items['short_term_disability']
        self.opers = paycheck_items['opers']
        self.four_01k = paycheck_items['four_01k']
        self.four_57b = paycheck_items['four_57b']
        self.net_pay = paycheck_items['net_pay']
        self.schwab_deposit = paycheck_items['schwab_deposit']
        self.fifth_third_deposit = paycheck_items['fifth_third_deposit']
        self.hsa_contribution = paycheck_items['hsa_contribution']
        self.fsa_contribution = paycheck_items['fsa_contribution']
        try:
            self.total_health_insurance = paycheck_items['health_insurance'] + paycheck_items['vision_insurance'] + paycheck_items['dental_insurance']
        except KeyError:
            self.total_health_insurance = 0.0


@logger.catch
def kat_paycheck(file):
    """With kat's paycheck the lines vary based on earnings throughout the year - the personal holiday moved all lines down one, so need
    to figure out a way to address this, same issue probably for Justin."""
    df = tb.read_pdf(file, area=(0,0 , 612, 792), columns=[150, 210, 288], stream=True, guess=True, pages='1', pandas_options={'header': None})
    print(df)
    pay_dict = {
        "kat_gross_pay": clean_data(df[0].loc[16, 2]),
        "justin_gross_pay": 0.0,
        "federal_tax": clean_data(df[0].loc[19, 2]),
        "social_security": clean_data(df[0].loc[21, 2]),
        "medicare": clean_data(df[0].loc[22, 2]),
        "ohio_tax": clean_data(df[0].loc[23, 2]),
        "city_tax": clean_data(df[0].loc[24, 2]),
        "short_term_disability": clean_data(df[0].loc[27, 2]),
        "four_01k": clean_data(df[0].loc[28, 2]),
        "four_57b": 0.0,
        "opers": 0.0,
        "net_pay": clean_data(df[0].loc[29, 2]),
        "schwab_deposit": clean_data(df[0].loc[30, 2]),
        "fifth_third_deposit": clean_data(df[0].loc[31, 2])
    }
    return pay_dict


@logger.catch
def justin_paycheck(file):
    PAY_ITEMS_DICT = {
        "HEALTH": total_health_data,
        "DENTAL": total_dental_data,
        "DEF COMP": four_57b_data,
        "OPERS": opers_data,
        "VISION": total_vision_data,
        "HSA EE": hsa_contribution,
        "FLEX DEP": fsa_contribution,
    }
    df = tb.read_pdf(file, area=(0,0 , 612, 792), columns=[390, 440, 475, 515, 590], stream=True, guess=True, pages='1', pandas_options={'header': None})
    print(df)
    for row in range(16):
        for key in PAY_ITEMS_DICT.keys():
            if df[0].loc[row, 0] == key:
                column_1_value = df[0].loc[row, 1]
                print(f"{key} is: {column_1_value}")
                PAY_ITEMS_DICT[key] = clean_data(df[0].loc[row, 1])


    pay_dict = {
        "justin_gross_pay": clean_data(df[0].loc[35, 3]),
        "kat_gross_pay": 0.0,
        "federal_tax": clean_data(df[0].loc[6, 1]),
        "social_security": 0.0,
        "medicare": clean_data(df[0].loc[5, 1]),
        "ohio_tax": clean_data(df[0].loc[7, 1]),
        "city_tax": clean_data(df[0].loc[8, 1]),
        "short_term_disability": 0.0,
        "four_01k": 0.0,
        "four_57b": four_57b_data,
        "opers": opers_data,
        "net_pay": clean_data(df[0].loc[36, 3]),
        "schwab_deposit": clean_data(df[0].loc[21, 4]),
        "fifth_third_deposit": clean_data(df[0].loc[22, 4]),
        "health_insurance": total_health_data,
        "vision_insurance": total_vision_data,
        "dental_insurance": total_dental_data,
        "hsa_contribution": hsa_contribution,
        "fsa_contribution": fsa_contribution,
    }
    return pay_dict

@logger.catch
def clean_data(string):
    filter_object = filter(str.isdigit, string)
    new_string = "".join(filter_object)
    new_string = float(new_string)/100
    return new_string

@logger.catch
def sum_gross_pay(paycheck_list):
    justin_gross_pay = 0.0
    kat_gross_pay = 0.0
    federal_tax = 0.0
    social_security = 0.0
    medicare = 0.0
    ohio_tax = 0.0
    city_tax = 0.0
    short_term_disability = 0.0
    opers = 0.0
    four_01k = 0.0
    four_57b = 0.0
    net_pay = 0.0
    schwab_deposit = 0.0
    fifth_third_deposit = 0.0
    health_insurance = 0.0
    dental_insurance = 0.0
    vision_insurance = 0.0
    total_insurance = 0.0
    hsa_contribution = 0.0
    fsa_contribution = 0.0
    for paycheck in paycheck_list:
        justin_gross_pay += paycheck.justin_gross_pay
        kat_gross_pay += paycheck.kat_gross_pay
        print("TEST: " + str(paycheck.federal_tax))
        federal_tax += paycheck.federal_tax
        social_security += paycheck.social_security
        medicare += paycheck.medicare
        ohio_tax += paycheck.ohio_tax
        city_tax += paycheck.city_tax
        short_term_disability += paycheck.short_term_disability
        opers += paycheck.opers
        four_01k += paycheck.four_01k
        four_57b += paycheck.four_57b
        net_pay += paycheck.net_pay
        schwab_deposit += paycheck.schwab_deposit
        fifth_third_deposit += paycheck.fifth_third_deposit
        total_insurance += paycheck.total_health_insurance
        hsa_contribution += paycheck.hsa_contribution
        fsa_contribution += paycheck.fsa_contribution
    print("Justin Gross Pay: " + str(justin_gross_pay))
    print("Kat Gross Pay: " + str(kat_gross_pay))
    print("Federal Tax: " + str(federal_tax))
    print("Social Security: " + str(social_security))
    print("Medicare: " + str(medicare))
    print("Ohio Tax: " + str(ohio_tax))
    print("City Tax: " + str(city_tax))
    print("Short Term Disability: " + str(short_term_disability))
    print("OPERS: " + str(opers))
    print("401k: " + str(four_01k))
    print("457b: " + str(four_57b))
    print("Net Pay: " + str(net_pay))
    print("Schwab Deposit: " + str(schwab_deposit))
    print("Fifth Third Deposit: " + str(fifth_third_deposit))
    print("Total Insurance: " + str(total_insurance))
    print(f"HSA Contribution: {hsa_contribution}")
    print(f"FSA Contribution: {fsa_contribution}")


paycheck_list = []
# The files list below is a list comprehension to make sure the directory isn't added as an object.
files = [file for file in os.listdir(DIRECTORY) if os.path.isfile(os.path.join(DIRECTORY, file))]
for file in files:
    print(file[:3])
    if file[:3] == "Cit":
        pay_dict = justin_paycheck(PATH + file)
        paycheck = Paycheck(pay_dict)
    elif file[:3] == "Pay":
        pay_dict = kat_paycheck(PATH + file)
        paycheck = Paycheck(pay_dict)
    paycheck_list.append(paycheck)

print(paycheck_list)
sum_gross_pay(paycheck_list)

# if df[0].loc[row, 0] == "HEALTH":
#     # print("Health is: " + str(df[0].loc[row, 1]))
#     total_health_data = clean_data(df[0].loc[row, 1])
# if df[0].loc[row, 0] == "DENTAL":
#     # print("Dental is: " + str(df[0].loc[row, 1]))
#     total_dental_data = clean_data(df[0].loc[row, 1])
# if df[0].loc[row, 0] == "DEF COMP":
#     # print("Def Comp is: " + str(df[0].loc[row, 1]))
#     four_57b_data = clean_data(df[0].loc[row, 1])
#     # print(four_57b_data)
# if df[0].loc[row, 0] == "OPERS":
#     print("OPERS is: " + str(df[0].loc[row, 1]))
#     opers_data = clean_data(df[0].loc[row, 1])
# if df[0].loc[row, 0] == "VISION":
#     # print("Vision is: " + str(df[0].loc[row, 1]))
#     total_vision_data = clean_data(df[0].loc[row, 1])
# if df[0].loc[row, 0] == "HSA EE":
#     print("HSA contribution is: " + str(df[0].loc[row, 1]))
#     hsa_contribution = clean_data(df[0].loc[row, 1])
# if df[0].loc[row, 0] == "FLEX DEP":
#     print("FSA contribution is: " + str(df[0].loc[row, 1]))
#     fsa_contribution = clean_data(df[0].loc[row, 1])
