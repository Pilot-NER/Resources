import csv
import nltk
from geotext import GeoText

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
def map_memo_to_location(memos_list):
    memo_to_location_dict = dict()
    for memo in memos_list:
        str = GeoText("Yes")
        memo_to_location_dict[memo] = str.cities
    return memo_to_location_dict

print(map_memo_to_location(yong_memos_list))