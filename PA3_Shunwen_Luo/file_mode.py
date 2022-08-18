import argparse
import csv
from collections import defaultdict
import os
# Helper function to read the test file
# Feel free to change based on the desired data type you want to use to store the data
def read_file(file_path,filePath):
    with open(os.path.join(filePath,file_path)) as f:
        reader = csv.reader(f)
        content = list(reader)
    return content

def jud(li):
# Determining the rank to which an individual's holdings belong
# The lower the ranking is the winner.
    suit=[]
    number=[]
    for i in range(1,len(li)):
        suit.append(li[i][0])
        number.append(int(li[i][1:]))
    number=[14 if i == 1 else i for i in number]
    slen=len(set(suit))
    nlen=len(set(number))
    ndict = {}
    for key in number:
        ndict[key] = ndict.get(key, 0) + 1
    dif=max(ndict.values())- min(ndict.values())

    if slen == 1 and sorted(number)==[10, 11, 12, 13, 14]:
        return 0
    elif slen == 1 and nlen == 5 and int(max(number)) - int(min(number)) == 4 and max(number)!= 14:
        return 1
    elif nlen == 2 and dif == 3:
        return 2
    elif nlen == 2 and dif == 1:
        return 3
    elif slen == 1:
        return 4
    elif nlen == 5 and int(max(number)) - int(min(number)) == 4:
        return 5
    elif nlen == 3 and dif == 2:
        return 6
    elif nlen == 3 and dif == 1:
        return 7
    elif nlen == 4 and dif == 1:
        return 8
    else:
        return 9

def main(dir):
    '''parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str, 
                    help='A required path to the test file')
    parser.add_argument('--result', type=str, required=False,
                    help='The IDs for the expected winner(s), separated by comma')
    args = parser.parse_args()'''
    filelist = os.listdir(dir)
    filelist.sort(key=lambda x:int(x[:-4]))
    f = open("test_results.txt")
    counter=0
    check_list=[]
    result_list=[]
    for file in filelist:
        #print(check(file,dir)[1])
        check_list.append(int(check(file,dir)[1]))
    for line in f:
        b=line.split(',')
        b[1]=b[1].strip('\n')
        result_list.append(int(b[1]))
    #print(check_list)
    #print(result_list)
    for i in range(len(check_list)):
        #print(check_list[i])
        #print(result_list[i])
        if check_list[i] == result_list[i]:
            counter+=1
    return counter





def check(fi,dirc):
    tlist=read_file(fi,dirc) #Read the file
    pdict = {}
    wdict = {}
    #print(tlist)
    for i in range(len(tlist)):
        pdict[i] = jud(tlist[i])   #Get the rank
    #print(pdict)
    rank = min(pdict.values())
    for key, value in pdict.items():
        if (value == min(pdict.values())):
            for i in tlist:
                if i[0] == str(key):
                    wdict[key] = i[1:]
    #print(rank)
    #print(wdict)
    #print('Winner:', end=" ")
# If there is a tie, determine who is the winner
    if rank==0:
        return str(rank0(wdict))
    elif rank==1:
        return str(rank1(wdict))
    elif rank==2:
        return str(rank2(wdict))
    elif rank==3:
        return str(rank3(wdict))
    elif rank==4:
        return str(rank4(wdict))
    elif rank==5:
        return str(rank5(wdict))
    elif rank==6:
        return str(rank6(wdict))
    elif rank==7:
        return str(rank7(wdict))
    elif rank==8:
        return str(rank8(wdict))
    elif rank==9:
        return str(rank9(wdict))

# Followings are functions to determine the tie-breaker.
def rank0(dic):
    w=[]
    #If rank is 0, judge the winner
    for i in dic.keys():
        w.append(i)
    return w

def rank1(dic):
    # If rank is 1, judge the winner
    w = []
    cdict = {}
    for key, value in dic.items():
        number = []
        for i in value:
            number.append(int(i[1:]))
        cdict[key] = max(number)
    for ckey, cvalue in cdict.items():
        if cvalue == max(cdict.values()):
            w.append(ckey)
    return w
def rank2(dic):
    # If rank is 2, judge the winner
    w = []
    cdict = {}
    for key, value in dic.items():
        number = []
        for i in value:
            number.append(int(i[1:]))
        real = [14 if i == 1 else i for i in number]
        tdict = {}
        for i in real:
            tdict[key] = tdict.get(i, 0) + 1
        for tkey, tvalue in tdict.items():
            if tvalue == 1:
                cdict[key] = tkey
    if 1 in cdict.values():
        for ckey, cvalue in cdict.items():
            w.append(ckey)
    else:
        for ckey, cvalue in cdict.items():
            if cvalue == max(cdict.values()):
                w.append(ckey)
    return w
def rank3(dic):
    # If rank is 3, judge the winner
    w = []
    cdict1 = {}
    cdict2 = {}
    for key, value in dic.items():
        number = []
        for i in value:
            number.append(int(i[1:]))
        real = [14 if i == 1 else i for i in number]
        tdict = {}
        for i in real:
            tdict[i] = tdict.get(i, 0) + 1
        for tkey, tvalue in tdict.items():
            if tvalue == 3:
                cdict1[key] = tkey
            elif tvalue == 2:
                cdict2[key] = tkey
    if len(set(cdict1.values())) == 1:
        for ckey, cvalue in cdict2.items():
            if cvalue == max(cdict2.values()):
                w.append(ckey)
    else:
        for ckey, cvalue in cdict1.items():
            if cvalue == max(cdict1.values()):
                w.append(ckey)
    return w
def rank4(dic):
    # If rank is 4, judge the winner
    w = []
    cdict = {}
    for key, value in dic.items():
        number = []
        for i in value:
            number.append(int(i[1:]))
        real = [14 if i == 1 else i for i in number]
        cdict[key] = sorted(real, reverse=True)
    for i in cdict.values():
        a = list(cdict.values())[0]
        if i > a:
            a = i
    for k, v in cdict.items():
        if v == a:
            w.append(k)
    return w
def rank5(dic):
    # If rank is 5, judge the winner
    w = []
    cdict = {}
    for key, value in dic.items():
        number = []
        for i in value:
            number.append(int(i[1:]))
        real = [14 if i == 1 else i for i in number]
        cdict[key] = real[0]
    for i in cdict.values():
        a = list(cdict.values())[0]
        if i > a:
            a = i
    for k, v in cdict.items():
        if v == a:
            w.append(k)
    return w
def rank6(dic):
    # If rank is 6, judge the winner
    w = []
    cdict1 = {}
    cdict2 = defaultdict(list)
    for key, value in dic.items():
        number = []
        for i in value:
            number.append(int(i[1:]))
        real = [14 if i == 1 else i for i in number]
        tdict = {}
        for i in real:
            tdict[i] = tdict.get(i, 0) + 1
        for tkey, tvalue in tdict.items():
            if tvalue == 3:
                cdict1[key] = tkey
            elif tvalue == 1:
                cdict2[key].append(tkey)
    if len(set(cdict1.values())) == 1:
        for i in cdict2.values():
            a = list(cdict2.values())[0]
            if i > a:
                a = i
        for k, v in cdict2.items():
            if v == a:
                w.append(k)
    else:
        for ckey, cvalue in cdict1.items():
            if cvalue == max(cdict1.values()):
                w.append(ckey)
    return w
def rank7(dic):
    # If rank is 7, judge the winner
    w = []
    cdict1 = defaultdict(list)
    cdict2 = defaultdict(list)
    for key, value in dic.items():
        number = []
        for i in value:
            number.append(int(i[1:]))
        real = [14 if i == 1 else i for i in number]
        tdict = {}
        for i in real:
            tdict[i] = tdict.get(i, 0) + 1

        for tkey, tvalue in tdict.items():
            if tvalue == 2:
                cdict1[key].append(tkey)
            elif tvalue == 1:
                cdict2[key].append(tkey)
    b_set = set(map(tuple, cdict1.values()))
    if len(b_set) == 1:
        for i in cdict2.values():
            a = list(cdict2.values())[0]
            if i > a:
                a = i
        for k, v in cdict2.items():
            if v == a:
                w.append(k)
    else:
        for i in cdict1.values():
            a = list(cdict1.values())[0]
            if i > a:
                a = i
        for k, v in cdict1.items():
            if v == a:
                w.append(k)
    return w
def rank8(dic):
    # If rank is 8, judge the winner
    w = []
    cdict1 = defaultdict(list)
    cdict2 = defaultdict(list)
    for key, value in dic.items():
        number = []
        for i in value:
            number.append(int(i[1:]))
        real = [14 if i == 1 else i for i in number]
        tdict = {}
        for i in real:
            tdict[i] = tdict.get(i, 0) + 1
        for tkey, tvalue in tdict.items():
            if tvalue == 2:
                cdict1[key].append(tkey)
            elif tvalue == 1:
                cdict2[key].append(tkey)
    b_set = set(map(tuple, cdict1.values()))
    b = map(list, b_set)
    if len(b_set) == 1:
        for i in cdict2.values():
            a = list(cdict2.values())[0]
            if i > a:
                a = i
        for k, v in cdict2.items():
            if v == a:
               w.append(k)
    else:
        for i in cdict1.values():
            a = list(cdict1.values())[0]
            if i > a:
                a = i
        for k, v in cdict1.items():
            if v == a:
                w.append(k)
    return w
def rank9(dic):
    # If rank is 9, judge the winner
    w = []
    cdict = {}
    for key, value in dic.items():
        number = []
        for i in value:
            number.append(int(i[1:]))
        real = [14 if i == 1 else i for i in number]
        cdict[key] = real
    a=[]
    for i in cdict.values():
        #print(i)
        a = list(cdict.values())[0]
        a.sort(reverse=True)
        i.sort(reverse=True)
        if i > a:
            a = i
    for k, v in cdict.items():
        if v == a:
            w.append(k)
    return w
