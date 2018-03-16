import csv
import nltk
from GeoExtraction import geoextraction

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
        memos_list.append(row[MEMO_STRING]) # lists of memo (exclude vendors)
        vendors_list.append(row[VENDOR].lstrip('[\'').rstrip('\']')) # lists of vendors
        memo_to_vendor_dict[row[MEMO_STRING]] = row[VENDOR].lstrip('[\'').rstrip('\']')  # dictionary of memos mapped to vendors

# I only analyze memos from 200th till 343th
yong_memos_list = memos_list[200:]
yong_vendors_list = vendors_list[200:]

# Extract location
y = geoextraction.GeoExtraction(yong_memos_list[1])
print(y.location())