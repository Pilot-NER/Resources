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
    for mem in memos_list:
        # memos less than or equal to three words are left alone
        if len(mem.split()) <= 3
            pass ##### or would it be break?
        else:
            #remove abbreviations such as debt car/credit card, ref, crd, dt number, Paypal, etc.
            shorthands = "(?i)debit card|credit card|debit|credit|card|crd|ref|cashier check purchase|paypal"
            mem = re.sub(' +',' ',re.sub(shorthands, '', mem))
remove_abr(memos_list)


def get_location(memos_list):
    # We need a new list or something with locations for each vendor (would it be a hashmap?)
    abr_loc = ["Bay","SFBA","San Franc","San Franciscoca","San Francis","San fransis","sf","San Fran","Frisco","S.F.","etc."]
        #use csv file for above
    location = {}
    for mem in memos_list:
        if any(x in mem for x in abr_loc):
        if abr_loc in mem:
            location = dict.fromkeys(['Bay', 'SFBA'], "Bay Area")
            my_dict.update(dict.fromkeys(['b', 'e'], 20))
            dict = dict.fromkeys(seq, 10)
