import csv
import re  # regex
import pprint
# import numpy as np
from GeoExtraction.geoextraction import GeoExtraction
from difflib import SequenceMatcher

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

# making results list
results = memos_list


# checking similarity
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

# algorithm functions
def ext1(data_list):
    # anything in quotation marks = name
    match_list = []
    for x in range(len(memos_list)):
        matches=re.findall(r'\"(.+?)\"',memos_list[x])
        if matches != [] and len(matches) == 1:
            memos_list[x].replace(matches[0], '')
            match_list.append(matches)
        else:
            match_list.append('X')
    return(match_list)

def ext2(data_list):
# repeated words = name
    rep_list = []
    for data in data_list:
        name =  ''
        words = data.split()
        counts = {}
        for word in words:
            if word not in counts:
                counts[word] = 1
            else:
                counts[word] += 1
            if counts[word] > 1:
                name += ' ' + word
        if not(name == ""):
            rep_list.append(name)
        else:
            rep_list.append('X')
    return(rep_list)

def ext3(memos_list):
    # memo length <=3 >> whole memo = name
    name_list = []
    L_removed = []
    num_location = "[^\s]*\d\d\d[^\s]*|\sCA\s"  # numbers or "CA" california
    for i, m in enumerate(memos_list):
        tmp = m.split()
        if len(tmp) <= 3:
            tmp_s = re.sub(num_location, "", m)
            name_list.append(tmp_s.lstrip().rstrip())
            L_removed.append(i)
        else:
            name_list.append('X')
    memos_list = [m for i, m in enumerate(memos_list) if i not in L_removed]
    return(name_list)

def sim1(memos_list):
    sim_list = []
    # remove financial shorthand
    for i, mem in enumerate(memos_list):
        # memos less than or equal to three words are left alone
        if len(mem.split()) <= 3:
            sim_list.append('pass')
        else:
            #remove abbreviations such as debt car/credit card, ref, crd, dt number, Paypal, etc.
            shorthands = "(?i)debit card|credit card|debit|credit|card|crd|ref|cashier check purchase|paypal| NY | New York | Las Vegas | NV | San Francisco | SF | San Francis |San Mateo | San Jose | Port Melbourn | CA | JAMAICA | Sydney | NS | Log Angeles | AU | Surry Hills | Singapore | SG "
            memN = re.sub(' +',' ',re.sub(shorthands, '', mem))
            if mem == memN:
                sim_list.append('X')
            else:
                sim_list.append(memN)
    return sim_list

def sim1x(memos_list):
    changed_list = []
    for i, mem in enumerate(memos_list):
        # memos less than or equal to three words are left alone
        if len(mem.split()) <= 3:
            changed_list.append(mem)
        else:
            #remove abbreviations such as debt car/credit card, ref, crd, dt number, Paypal, etc.
            shorthands = "(?i)debit card|credit card|debit|credit|card|crd|ref|cashier check purchase|paypal| NY | New York | Las Vegas | NV | San Francisco | SF | San Francis |San Mateo | San Jose | Port Melbourn | CA | JAMAICA | Sydney | NS | Log Angeles | AU | Surry Hills | Singapore | SG "
            mem = re.sub(' +',' ',re.sub(shorthands, '', mem))
            changed_list.append(mem)
    return changed_list

def sim2(memos_list):
    #reomve mixed alphanumerics
    num = "[^s]*\d\d\d\d\d+[^s]*"  # more than 5 numbers
    alt_alphanum = "(?i)[^s][a-z]+\d+\w*[^s]"  # alternating numbers and alphabets (alphabets come first)
    alt_alphanum_2 = "(?i)[^s]\d+[a-z]+\w*[^s]"  # alternating numbers and alphabets (numbers come first)
    L = list()
    for m in memos_list:
        tmp = re.split(num + "|" + alt_alphanum + "|" + alt_alphanum_2, m)
        tmp = [x.lstrip().rstrip() for x in tmp]
        tmp = ' '.join(tmp).lstrip().rstrip()
        # print(m, tmp)
        if tmp:
            L.append(tmp)
        else:
            L.append('X')
    return L

def sim2x(memos_list):
    num = "[^s]*\d\d\d\d\d+[^s]*"  # more than 5 numbers
    alt_alphanum = "(?i)[^s][a-z]+\d+\w*[^s]"  # alternating numbers and alphabets (alphabets come first)
    alt_alphanum_2 = "(?i)[^s]\d+[a-z]+\w*[^s]"  # alternating numbers and alphabets (numbers come first)

    L = list()

    for m in memos_list:
        tmp = re.split(num + "|" + alt_alphanum + "|" + alt_alphanum_2, m)
        tmp = [x.lstrip().rstrip() for x in tmp]
        tmp = ' '.join(tmp).lstrip().rstrip()
        # print(m, tmp)
        if tmp:
            L.append(tmp)
        else:
            L.append(m)
    return L

def ext4(memos_list):
    # word before company suffixes = name
    keywords = ["(?i)\sinc.\s", "(?i)\sLLC\s", "(?i)\sCO\s", "(?i)\sLimited\s", "(?i)\sINC\s", "(?i)\sCorporation\s",
                "(?i)\s.com\s", "(?i)\s.net\s"]
    ans = list()
    new_memos = list()
    for m in memos_list:
        for k in keywords:
            tmp = re.split(k, m)
            if len(tmp) > 1 and (m not in ans or (m in ans and len(tmp[0]) < len(ans[m]))):
                ans.append(tmp[0] + " " + k[6:-2])
            else:
                new_memos.append(m)
                ans.append('X')
    return ans

def pend1(memos_list):
    # extract location terms
    new_memos, location_dict = list(), dict()
    G = GeoExtraction()
    count = 0
    for m in memos_list:
        l = G.extract_location(m)
        new_m = G.remove_location(m)
        new_memos.append(m)
        location_dict[new_m] = l
        print(count)
        count += 1
    return new_memos, location_dict

def sim3(memos_list):
    # remove the date/ref/crd number (assumed format of date - "MM/DD")
    date = "[^\s]*\d\d/\d\d[^\s]*"  # date
    ref = "(?i)[^\s]*ref[\d^\s]*"  # reference number in format "REF...""
    crd = "(?i)[^\s]*crd[\d^\s]*"  # credit number in format "CRD..."
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
        if tmp == memo:
            new_list.append('X')
        else:
            new_list.append(tmp)
    return new_list

def sim3x(memos_list):
    # remove the date from the string (assume format - "MM/DD")

    date = "[^\s]*\d\d/\d\d[^\s]*"  # date
    ref = "(?i)[^\s]*ref[\d^\s]*"  # reference number in format "REF...""
    crd = "(?i)[^\s]*crd[\d^\s]*"  # credit number in format "CRD..."
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

def sim4(memos_list):
    # ignore online/bank transfers
    sim_list = []
    for x in memos_list:
        if 'internet transfer' in x.lower():
            sim_list.append('Rm')
        elif 'online transfer' in x.lower():
            sim_list.append('Rm')
        else:
            sim_list.append('X')
    return(sim_list)

def sim4x(memos_list):
    # 12. removing transfers
    changed_list = []
    for x in range(len(memos_list)):
        if 'internet transfer' in memos_list[x].lower():
            changed_list.append('X')

        elif 'online transfer' in memos_list[x].lower():
            changed_list.append('X')
        else:
            changed_list.append(memos_list[x])
    return(changed_list)

# testing

ori = ['memo']+memos_list
simp_list = sim1x(sim2x(sim3x(sim4x(ori))))
simp_list[0] = "simp"
sim1 = ['sim1']+sim1(memos_list)
sim2 = ['sim2']+sim2(memos_list)
sim3 = ['sim3']+sim3(memos_list)
sim4 = ['sim4']+sim4(memos_list)
ext1 = ['ext1']+ext1(simp_list)
ext2 = ['ext2']+ext2(simp_list)
ext3 = ['ext3']+ext3(simp_list)
ext4 = ['ext4']+ext4(simp_list)

'''
print(len(memos_list))
print(len(ori))
print(len(simp_list))
print(len(sim1))
print(len(sim2))
print(len(sim3))
print(len(sim4))
print(len(ext1))
print(len(ext2))
print(len(ext3))
print(len(ext4))
'''

print(memos_list)

testfile = 'test.csv'
# checking for no extraction

with open(testfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for x in range(len(ori)):
        writer.writerow([ori[x],simp_list[x]])

extF = ['failed']
for x in range(len(ori)):
    if ext1[x] == ext2[x] == ext3[x] == ext4[x] == 'X':
        extF.append('X')
    else:
        extF.append('extracted')

csvfile = 'tracking.csv'

with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for x in range(len(ori)):
        writer.writerow([ori[x],sim1[x],sim2[x],sim3[x],sim4[x],simp_list[x],ext1[x],ext2[x],ext3[x],ext4[x],extF[x]])

def check_accuracy(ans_list,my_list):
    acc_list = []
    for x in range(len(ans_list)):
        acc_list.append(similar(ans_list[x],my_list[x]))
    return(acc_list)

#print(similar("apple","appel"))
#print(similar("apple","mango"))
#print(check_accuracy(vendors_list,ext2[1:]))
#print(vendors_list)
#print(ext2[1:])
#print(len(vendors_list))
#print(len(ext2[1:]))


def test(data_list):
    ind_col = ['memo'] + data_list
    ext2_col = ['ext2']
    for memo in data_list:
        res = ext2(memo)
        if res[0]:
            ext2_col.append(res[1])
        else:
            ext2_col.append('X')
    return(np.column_stack((np.array(ind_col),np.array(ext2_col))))
