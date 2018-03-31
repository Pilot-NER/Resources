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

def remove_abr(memos_list, vendors_list, memo_to_vdendor_dict):
    #remove abbreviations such as debt car/credit card, ref, crd, dt number, Paypal, etc.
    for i in len(memos_list):
        if len(memos_list[i].split()) <= 3
            pass
        else:
            if memos_list[i] = re.sub("Debit Card", '', memos_list[i])

analyze_pattern1(memos_list, vendors_list, memo_to_vendor_dict)
