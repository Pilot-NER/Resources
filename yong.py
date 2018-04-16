import csv
import re  # regex
import pprint
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
        memo_to_vendor_dict[row[MEMO_STRING]] = row[VENDOR].lstrip('[\'').rstrip(
            '\']')  # dictionary of memos mapped to vendors


# algorithm 11/4
def remove_date_ref_Crd(memos_list):
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



memos_list_wo_date = remove_date_ref_Crd(memos_list)



# algorithm 2
def extract_repeated(memos_list):
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
            names.append(tmp_str.rstrip())
        else:
            new_memos.append(memo)
    return new_memos, names


# algorithm 3
def less_than_3(memos_list):
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


# algorithm 4: remove abbreviations such as debt car/credit card, ref, crd, dt number, Paypal, etc.
def remove_abr(memos_list):
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



# algorithm 6/13
def remove_numbers_mixed_alphanumerics(memos_list):
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

# algorithm 9
def before_keywords(memos_list):
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

# algorithm 10
def return_and_remove_location(memos_list):
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

# algorithm 12
def analyze_pattern12(memos_list):
    # 12. removing transfers
    for x in memos_list:
        if 'internet transfer' in x.lower():
            del memos_list[memos_list.index(x)]

        elif 'online transfer' in x.lower():
            del memos_list[memos_list.index(x)]
    return(memos_list)


def analyze_pattern1(memos_list):
    match_list = []
    for x in range(len(memos_list)):
        matches=re.findall(r'\"(.+?)\"',memos_list[x])
        if matches != [] and len(matches) == 1:
            memos_list[x].replace(matches[0], '')
            match_list.append(matches)
    return(memos_list,match_list)

def analyze_pattern8(memos_list):
    name_list = []
    for x in range(len(memos_list)):
        if memos_list[x].count('*') == 1:
            name = memos_list[x][memos_list[x].find('*')+1:]
            name_list.append(name)
            memos_list[x].replace(name, '')
    return(memos_list, name_list)


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

