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

def remove_date_ref_Crd(memos_list, vendors_list, memo_to_vendor_dict):
	# remove the date from the string (assume format - "MM/DD")
	
	date = "[^\s]*\d\d/\d\d[^\s]*" 	# date
	ref = "(?i)ref[\d^\s]*"		   	# reference number in format "REF...""	
	crd = "(?i)crd[\d^\s]*"		   	# credit number in format "CRD..."		
	# num = "[^\s]*\d\d\d\d+[^\s]*"

	new_list = []
	for i, memo in enumerate(memos_list):
		tmp = re.split(date, memo)
		tmp = [x.lstrip().rstrip() for x in tmp]
		tmp = ' '.join(tmp).lstrip().rstrip()

		tmp = re.split(ref, tmp)
		tmp = [x.lstrip().rstrip() for x in tmp]
		tmp = ' '.join(tmp).lstrip().rstrip()

		tmp = re.split(crd, tmp)
		tmp = [x.lstrip().rstrip() for x in tmp]
		tmp = ' '.join(tmp).lstrip().rstrip()

		new_list.append(tmp)

	return new_list

memos_list_wo_date = remove_date_ref_Crd(memos_list, vendors_list, memo_to_vendor_dict)


# algorithm 9
def before_keywords(memos_list):
	keywords = ["(?i)\sinc.\s", "(?i)\sLLC\s", "(?i)\sCO\s", "(?i)\sLimited\s", "(?i)\sINC\s", "(?i)\sCorporation\s", "(?i)\s.com\s", "(?i)\s.net\s"]
	ans = dict()
	for m in memos_list:
		for k in keywords:
			tmp = re.split(k, m)
			if len(tmp) > 1 and (m not in ans or (m in ans and len(tmp[0]) < len(ans[m]))):
				ans[m] = tmp[0] + " " + k[6:-2]
	return ans

alg_9 = before_keywords(memos_list_wo_date)
# for m, k in alg_9.items():
# 	print(m, ":", k)


# algorithm 3
def less_than_3(memos_list):
	ans = dict()
	num_location = "[^\s]*\d\d\d[^\s]*|\sCA\s" # numbers or "CA" california
	for m in memos_list:
		tmp = m.split()
		if len(tmp) <=3:
			tmp_s = re.sub(num_location, "", m)
			ans[m] = tmp_s.lstrip().rstrip()

	return ans

print(less_than_3(memos_list_wo_date))





