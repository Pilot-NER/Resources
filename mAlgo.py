import csv

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
def analyze_pattern1(memos_list, vendors_list, memo_to_vdendor_dict):
    # removing transfers
    for x in range(len(memos_list)):
        if 'internet transfer' in memos_list[x].lower():
            sorted_list[x+1][2] = 'online transfer'

        elif 'online transfer' in memos_list[x].lower():
            sorted_list[x+1][2] = 'online transfer'
    return(1)

analyze_pattern1(memos_list, vendors_list, memo_to_vendor_dict)
#print(sorted_list)
#print(sorted_list[129])
