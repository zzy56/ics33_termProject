from collections import defaultdict

# Followings are functions to determine the tie-breaker.
def rank0(dic):
    #If rank is 0, judge the winner
    winner=[]
    for i in dic.keys():
        winner.append(i)
    return winner

def rank1(dic):
    # If rank is 1, judge the winner
    winner=[]
    cdict={}
    for key, value in dic.items():
        number = []
        for i in value:
            number.append(int(i[1:]))
        cdict[key] = max(number)
    for ckey, cvalue in cdict.items():
        if cvalue == max(cdict.values()):
            winner.append(ckey)
    return winner
def rank2(dic):
    # If rank is 2, judge the winner
    winner = []
    cdict = {}
    for key, value in dic.items():
        number = []
        for i in value:
            number.append(int(i[1:]))
        tdict = {}
        for key in number:
            tdict[key] = tdict.get(key, 0) + 1
        for tkey, tvalue in tdict.items():
            if tvalue == 1:
                cdict[key] = tkey
    if 1 in cdict.values():
        for ckey, cvalue in cdict.items():
            winner.append(ckey)
    else:
        for ckey, cvalue in cdict.items():
            if cvalue == max(cdict.values()):
                winner.append(ckey)
    return winner
def rank3(dic):
    # If rank is 3, judge the winner
    winner = []
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
                winner.append(ckey)
    else:
        for ckey, cvalue in cdict1.items():
            if cvalue == max(cdict1.values()):
                winner.append(ckey)
    return winner
def rank4(dic):
    # If rank is 4, judge the winner
    winner = []
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
            winner.append(k)
    return winner
def rank5(dic):
    # If rank is 5, judge the winner
    winner = []
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
            winner.append(k)
    return winner
def rank6(dic):
    # If rank is 6, judge the winner
    winner = []
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
                winner.append(k)
    else:
        for ckey, cvalue in cdict1.items():
            if cvalue == max(cdict1.values()):
                winner.append(ckey)
    return winner
def rank7(dic):
    # If rank is 7, judge the winner
    winner = []
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
                winner.append(k)
    else:
        for i in cdict1.values():
            a = list(cdict1.values())[0]
            if i > a:
                a = i
        for k, v in cdict1.items():
            if v == a:
                winner.append(k)
    return winner

def rank8(dic):
    # If rank is 8, judge the winner
    winner = []
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
                winner.append(k)
    else:
        for i in cdict1.values():
            a = list(cdict1.values())[0]
            if i > a:
                a = i
        for k, v in cdict1.items():
            if v == a:
                winner.append(k)
    return winner
def rank9(dic):
    # If rank is 9, judge the winner
    winner = []
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
            winner.append(k)
    return winner
