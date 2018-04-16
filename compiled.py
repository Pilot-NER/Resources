import csv
import re  # regex
import pprint
import numpy
from GeoExtraction.geoextraction import GeoExtraction

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

# algorithm functions
def ext1(data):
    # anything in quotation marks = name
    matches=re.findall(r'\"(.+?)\"',data)
    if matches != [] and len(matches) == 1:
        return([True, matches[0]])
    else:
        return([False])

def ext2(data):
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
        return([True,name])
    else:
        return([False])

    # anything repeated twice = name
    names = []
    new_memos = []
    for memo in memos_list:
        m = memo.split()
        tmp_set = set()
        tmp_str = ""
        for c in m:
            if c in tmp_set and c:
                tmp_str += c
                tmp_str += " "
            else:
                tmp_set.add(c)
        if tmp_str:
            print('y')
            return([True,tmp_str.rstrip()])
            #names.append(tmp_str.rstrip())
        else:
            return([False])
            #new_memos.append(memo)

def ext3(memos_list):
    # memo length <=3 >> whole memo = name
    ans = list()
    L_removed = list()
    num_location = "[^\s]*\d\d\d[^\s]*|\sCA\s"  # numbers or "CA" california
    for i, m in enumerate(memos_list):
        tmp = m.split()
        if len(tmp) <= 3:
            tmp_s = re.sub(num_location, "", m)
            ans.append(tmp_s.lstrip().rstrip())
            L_removed.append(i)
    memos_list = [m for i, m in enumerate(memos_list) if i not in L_removed]
    return memos_list, ans

def sim1(memos_list):
    # remove financial shorthand
    for i, mem in enumerate(memos_list):
        # memos less than or equal to three words are left alone
        if len(mem.split()) <= 3:
            pass ##### or would it be break?
        else:
            #remove abbreviations such as debt car/credit card, ref, crd, dt number, Paypal, etc.
            shorthands = "(?i)debit card|credit card|debit|credit|card|crd|ref|cashier check purchase|paypal| NY | New York | Las Vegas | NV | San Francisco | SF | San Francis |San Mateo | San Jose | Port Melbourn | CA | JAMAICA | Sydney | NS | Log Angeles | AU | Surry Hills | Singapore | SG "
            mem = re.sub(' +',' ',re.sub(shorthands, '', mem))
            memos_list[i] = mem
    return memos_list

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

    return new_memos, ans

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
        new_list.append(tmp)
    return new_list

def sim4(memos_list):
    # ignore online/bank transfers
    for x in memos_list:
        if 'internet transfer' in x.lower():
            del memos_list[memos_list.index(x)]

        elif 'online transfer' in x.lower():
            del memos_list[memos_list.index(x)]
    return(memos_list)

# testing

def test(data_list):
    ext2_col = ['ext2']
    for memo in data_list:
        res = ext2(memo)
        if res[0]:
            ext2_col.append(res[1])
        else:
            ext2_col.append('X')
    print(ext2_col)
    return(ext2_col)

print(memos_list)
test(memos_list)

'''
memos_list_wo_date = remove_date_ref_Crd(memos_list)
alg_14 = remove_numbers_mixed_alphanumerics(memos_list_wo_date)
alg_4 = remove_abr(memos_list)
alg_6 = remove_numbers_mixed_alphanumerics(alg_4)
alg_11 = remove_date_ref_Crd(alg_6)
alg_12 = analyze_pattern12(memos_list)
print(len(alg_4))  # == 338
print(len(alg_6))  # == 338
print(len(alg_11)) # == 338



alg_3, ans1 = less_than_3(alg_12)
alg_9, ans2 = before_keywords(alg_3)
alg_1, ans3 = analyze_pattern1(alg_9)
alg_8, ans4 = analyze_pattern8(alg_1)
alg_2, ans5 = extract_repeated(alg_8)
print(ans1)
print(ans2)
print(ans3)
print(ans4)
print(ans5)
print(set(alg_2))
'''
