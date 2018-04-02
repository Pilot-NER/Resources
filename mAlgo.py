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
        memos_list.append(row[MEMO_STRING])
        vendors_list.append(row[VENDOR].lstrip('[\'').rstrip('\']'))
        memo_to_vendor_dict[row[MEMO_STRING]] = row[VENDOR].lstrip('[\'').rstrip('\']')
        #sorted_list[0].append(row[MEMO_STRING])

# creating output table
sorted_list = [[0,0,0] for x in range(len(memos_list))]
sorted_list = [['memos','vendor_name','vendor_type']] + sorted_list
for x in range(len(memos_list)):
    sorted_list[x+1][0] = memos_list[x]

# functions to analyze the pattern
def analyze_pattern12(memos_list, vendors_list, memo_to_vdendor_dict):
    # 12. removing transfers
    for x in memos_list:
        if 'internet transfer' in x.lower():
            del memos_list[memos_list.index(x)]

        elif 'online transfer' in x.lower():
            del memos_list[memos_list.index(x)]
    return(memos_list)

def analyze_pattern1(memos_list, vendors_list, memo_to_vdendor_dict):
    # 1. quotation marks = name
    match_list = []
    for x in range(len(memos_list)):
        matches=re.findall(r'\"(.+?)\"',memos_list[x])
        if matches != [] and len(matches) == 1:
            memos_list[x].replace(matches, '')
            match_list.append(matches)
    return(memos_list,match_list)

    # 8. after * is NAME

    # !!! double repeated algo takes precedence as mre effective
    # !!! meaningless alphanumeric chains, dates, locations, common words (debit) need to be removed first
def analyze_pattern8(memos_list, vendors_list, memo_to_vdendor_dict):
    name_list = []
    for x in range(len(memos_list)):
        if memos_list[x].count('*') == 1:
            name = memos_list[x][memos_list[x].find('*')+1:]
            name_list.append(name)
            memos_list[x].replace(name, '')
    return(memos_list, name_list)


    # 10a. Abbreviations >> Full Name
def analyze_pattern10a(memos_list, vendors_list, memo_to_vdendor_dict):
    with open("Abbreviation Patterns - Sheet4.csv", 'r') as abbvfile:
        abbv = csv.reader(abbvfile)
        next(abbv)
        for row in abbv:
            abbv_to_name_dict[row[0]] = row[1]
    print(abbv_to_name_dict)

    for x in range(len(memos_list)):
        for y in abbv_to_name_dict.keys():
            if y in memos_list[x].lower():
                print(y)
                print(memos_list[x])
                if abbv_to_name_dict[y] != '':
                    #print(sorted_list[x+1])
                    sorted_list[x+1][0].replace(y,abbv_to_name_dict[y])
                    #print(sorted_list[x+1])

    return(1)
analyze_pattern8(memos_list, vendors_list, memo_to_vendor_dict)
'''
analyze_pattern12(memos_list, vendors_list, memo_to_vendor_dict)
analyze_pattern1(memos_list, vendors_list, memo_to_vendor_dict)
#print(sorted_list)
#print(sorted_list[129])
'''
