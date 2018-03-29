import csv
import re # regex
import pprint

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

def remove_date(memos_list, vendors_list, memo_to_vendor_dict):
	# remove the date from the string (assume format - "MM/DD")
	date = "[^\s]*\d\d/\d\d[^\s]*"
	new_list = []
	for i, memo in enumerate(memos_list):
		tmp = re.split(date, memo)
		tmp = [x.lstrip().rstrip() for x in tmp]
		new_list.append(' '.join(tmp).lstrip().rstrip())

	return new_list

memos_list_wo_date = remove_date(memos_list, vendors_list, memo_to_vendor_dict)
pprint.pprint(memos_list_wo_date)