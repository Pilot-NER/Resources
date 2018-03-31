import csv
import re

MEMO_STRING = 0
VENDOR = 1

# lists
memos_list = []
vendors_list = []

# dictionary
memo_to_vendor_dict = {}

with open("Sample memos - memos.csv", 'r') as memofile:
    memo = csv.reader(memofile)
    next(memo)  # skip the first line
    for row in memo:
        memos_list.append(row[MEMO_STRING])  # lists of memo (exclude vendors)
        vendors_list.append(row[VENDOR].lstrip('[\'').rstrip('\']'))  # lists of vendors
        memo_to_vendor_dict[row[MEMO_STRING]] = row[VENDOR].lstrip('[\'').rstrip('\']')  # dictionary of memos mapped to vendors


# functions to analyze the pattern
def remove_abr(memos_list):
    for i in memos_list:
        # memos less than or equal to three words are left alone
        if len(memos_list[i].split()) <= 3
            pass ##### or would it be break?
        else:
            #remove abbreviations such as debt car/credit card, ref, crd, dt number, Paypal, etc.
            shorthands = "(?i)debit card|credit card|debit|credit|card|crd|ref|cashier check purchase|paypal"
            memos_list[i] = re.sub(' +',' ',re.sub(shorthands, '', memos_list[i]))

remove_abr(memos_list)
