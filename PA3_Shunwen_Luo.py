#from cardTable import cardTable
import argparse
#import dealer
#import file_mode
#import tie_breaker
#from poker import poker
#from player import player
#from player import operationType
#from player import playerType
#from dealer import dealer
from enum import Enum
import random
#from pokerHands import pokerHands
import argparse
import csv
from collections import defaultdict
import os
from enum import Enum
import itertools
import random
#from pokerHands import pokerHands
#from pokerHandsType import pokerHandsType
from collections import defaultdict,Counter



class cardTable:
    def __init__(self):
        self.m_dealer = dealer()  # call dealer class
        self.__m_allPlayers = []
        self.__m_currentPlayers = []
        self.pokers = poker.creatPokerSet()
        self.communityCard = []
        self.winners = []
        self.maxbet=0

    def set_up_table(self, num):
        # Setting up the game environment
        self.addPlayer(player("User", playerType.human))
        for i in range(num):
            name = str(i + 1)
            self.addPlayer(player(name))

        self.refreshCurrentPlayers()

        while True:
            self.gameStart()
            self.shufflecard()
            for mplayer in self.__m_currentPlayers.copy():
                if mplayer.getplayerType() == playerType.human:
                    if mplayer.getMoney == 0:
                        return
            flag = int(input("1.Continue(Please enter 1)\n2.Exit (Please enter 2)\n:"))
            if flag == 2:
                return

    def gameStart(self):
        # main game function
        print('-----Game Start-----')
        self.deal()

        print('----- Round 1 -----')  # round 1

        for mplayer in self.__m_currentPlayers.copy():
            # mplayer.printPoker()
            if mplayer.getplayerType() == playerType.human:
                # print('Player', mplayer.getName(), ': rank', mplayer.__m_rank, 'bet $1')
                mplayer.printPoker()


        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        for mplayer in self.__m_currentPlayers.copy():
            if mplayer.getplayerType() == playerType.human:
                self.playerOperation(mplayer)
                #print('Player', mplayer.getName(), ': rank', mplayer.__m_rank, 'bet $1')


        for mplayer in self.__m_currentPlayers.copy():
            # mplayer.printPoker()
            if mplayer.getplayerType() != playerType.human:
                #print('Player', mplayer.getName(), ':bet $1')
                #mplayer.addbet(1)
                bet1 = mplayer.smartBet1()
                mplayer.addbet(bet1)
                print('Player', mplayer.getName(), ':bet $', bet1)
                #print('Player', mplayer.getName(), ': rank', mplayer.__m_rank, 'bet $1')
                # print(mplayer.getbet())

        self.addCommunityCard(3)
        self.printCommunityCard()

        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        for mplayer in self.__m_currentPlayers.copy():
            if mplayer.getplayerType() == playerType.human:
                self.playerOperation(mplayer)

        for mplayer in self.__m_currentPlayers.copy():
            # mplayer.printPoker()
            mplayer.__m_pokers, mplayer.__m_rank = mplayer.discardPoker(self.communityCard)
            # print('Player', mplayer.getName(), ': bet $1')
            if mplayer.getplayerType() != playerType.human:
                bet2=mplayer.smartBet2(mplayer.__m_rank,self.maxbet)
                mplayer.addbet(bet2)
                if self.maxbet<bet2:
                    self.maxbet=bet2
                print('Player', mplayer.getName(), ': bet $',bet2)
                # print(mplayer.getbet())

        print('----- Round 2 -----')  # round 2

        self.addCommunityCard(2)
        self.printCommunityCard()

        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        for mplayer in self.__m_currentPlayers.copy():
            if mplayer.getplayerType() == playerType.human:
                self.playerOperation(mplayer)

        for mplayer in self.__m_currentPlayers.copy():
            # mplayer.printPoker()
            mplayer.__m_pokers, mplayer.__m_rank = mplayer.discardPoker(self.communityCard)
            # print('Player', mplayer.getName(), ': bet $1')
            if mplayer.getplayerType() != playerType.human:
                if mplayer.__m_rank==9:
                    self.__m_currentPlayers.remove(mplayer)
                else:
                    bet3 = mplayer.smartBet3(mplayer.__m_rank, self.maxbet,self.communityCard)
                    mplayer.addbet(bet3)
                    if self.maxbet < bet3:
                        self.maxbet = bet3
                    print('Player', mplayer.getName(), ': bet $', bet3)



        self.judgingTiebreakers()

        winlist = [i.getName() for i in self.winners]
        totalbet = 0
        for mplayer in self.__m_allPlayers.copy():  # calculate for money
            totalbet += int(mplayer.getbet())
        # print(totalbet)

        for mplayer in self.__m_currentPlayers.copy():  # calculate for money
            if len(winlist) == len(self.__m_currentPlayers):
                break
            elif mplayer.getName() in winlist:
                mplayer.addMoney(totalbet / len(self.winners))
                mplayer.loseMoney(mplayer.getbet())
            else:
                mplayer.loseMoney(mplayer.getbet())

        print("——————Results————————")
        print('Winner: Player', ','.join(winlist))
        for mplayer in self.__m_allPlayers.copy():
            print("Player", mplayer.getName(), ":$", mplayer.getMoney())
            if mplayer.getMoney() <= 0:  # if someone's lose all money, remove from game
                print("Player", mplayer.getName(), "run out of money and is removed from the game.")
                self.__m_allPlayers.remove(mplayer)
        print("——————End of Game———————— ")

    def judgingTiebreakers(self):
        best_rank = min(self.__m_currentPlayers.copy(), key=lambda poker: poker.__m_rank)
        for mplayer in self.__m_currentPlayers.copy():
            if mplayer.__m_rank == best_rank.__m_rank:
                self.winners.append(mplayer)
        wdict = {}
        for i in self.winners:
            wdict[i.getName()] = i.getHandCards()

        # Judging Tiebreakers
        if best_rank == 0:
            self.winners =rank0(wdict)
        elif best_rank == 1:
            self.winners = rank1(wdict)
        elif best_rank == 2:
            self.winners =rank2(wdict)
        elif best_rank == 3:
            self.winners =rank3(wdict)
        elif best_rank == 4:
            self.winners = rank4(wdict)
        elif best_rank == 5:
            self.winners = rank5(wdict)
        elif best_rank == 6:
            self.winners = rank6(wdict)
        elif best_rank == 7:
            self.winners = rank7(wdict)
        elif best_rank == 8:
            self.winners =rank8(wdict)
        elif best_rank == 9:
            self.winners = rank9(wdict)

    def refreshCurrentPlayers(self):
        self.__m_currentPlayers.clear()
        for mplayer in self.__m_allPlayers:
            if mplayer.getMoney() > 0:
                self.__m_currentPlayers = self.__m_allPlayers.copy()

    def printCommunityCard(self):
        # print community card
        print("Community card :")
        for pok in self.communityCard:
            print(pok.getDecor(), pok.getPoint(), sep='', end=' ')
        print()

    def playerOperation(self, mplayer):

        type = mplayer.operation()
        if type == operationType.Discard:
            self.__m_currentPlayers.remove(mplayer)
            print(mplayer.getName(), ': fold')
        elif type == operationType.Filling:
            print(mplayer.getName(), ': add bet')
            a = input("How much you want to bet(please enter a number):")
            mplayer.addbet(int(a))
            #print(mplayer.getbet())
        # elif type == operationType.Pass:
        #  print(mplayer.getName(),': 过牌')
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

    def addCommunityCard(self, count: int):
        # add community card
        for i in range(count):
            self.communityCard.append(self.pokers.pop(0))

    def getPoker(self, pok):
        if len(self.pokers) <= 5:
            self.pokers.append(pok)

    def addPlayer(self, player):
        # add a player
        if len(self.__m_allPlayers) <= 8:
            self.__m_allPlayers.append(player)

    def deal(self):
        # distribute cards
        self.m_dealer.deal(self.pokers, self.__m_currentPlayers)

    def printPlayerInformation(self):
        print("--- Player information ---")
        for mplayer in self.__m_allPlayers:
            print('Name: ', mplayer.getName(), 'Money: ', mplayer.getMoney(), sep='', end=' ')

    def shufflecard(self):
        # shuffle card after a game
        for mplayer in self.__m_allPlayers:
            mplayer.clearPokers()
        self.refreshCurrentPlayers()
        self.communityCard.clear()
        self.winners.clear()
        self.pokers.clear()
        self.pokers = poker.creatPokerSet()

class dealer:
    # dealer to distribute cards
    def __init__(self):
        self.__m_pokerHands = pokerHands()
        pass

    def deal(self, pokers: list, players: list):
        random.shuffle(pokers)
        for i in range(len(players)):
            players[i].addPoker(pokers.pop(0))
            players[i].addPoker(pokers.pop(0))

    def compare(self, communityCard: list, players: list):
        for mplayer in players:
            cardlist = mplayer.getHandCards() + communityCard
            self.__m_pokerHands.getPokerHandsType(cardlist)

        pass

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
    rank = min(pdict.values())
    for key, value in pdict.items():
        if (value == min(pdict.values())):
            for i in tlist:
                if i[0] == str(key):
                    wdict[key] = i[1:]
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

class operationType(Enum):
    Discard = 1
    Filling = 2
    Pass = 3

class playerType(Enum):
    robot = 0
    human = 1

class player:
    # player class to store all player's information
    def __init__(self, name: str, playerType : playerType = playerType.robot):
        self.__m_pokers = []
        self.__m_name = name
        self.__m_money = 10
        self.__m_pokerHands = pokerHands()
        self.__m_playerType = playerType
        self.__m_bet=0
        pass

    def clearPokers(self):
        self.__m_pokers.clear()
    def getplayerType(self) -> playerType:
        return self.__m_playerType

    def getHandCards(self) -> list:
        return self.__m_pokers

    def getName(self) -> str:
        return self.__m_name

    def getMoney(self) -> int:
        return self.__m_money

    def loseMoney(self, money: int):
        self.__m_money = self.__m_money - int(money)

    def addMoney(self, money: int):
        self.__m_money = self.__m_money + money

    def addPoker(self, pok):
        if len(self.__m_pokers) <= 2:
            self.__m_pokers.append(pok)
    def getbet(self):
        return self.__m_bet

    def addbet(self,bet):
        self.__m_bet += bet

    def operation(self) -> operationType:
        if playerType.robot == self.__m_playerType:
            num = int(random.randint(1,3))
            return operationType(num)
        elif playerType.human == self.__m_playerType:
            if self.__m_money > 0:
                while True:
                    num = int(input("Please choose your option:\n1.fold(enter 1)\n2.bet (enter 2)\n"))
                    if num == 1 or num ==2 :
                        return operationType(num)
                    else:
                        print("Illegal operation")

    def discardPoker(self, communityCard) :
        # give a judgement to handpokers rank
        pokerlist = self.__m_pokers + communityCard
        a=min(itertools.combinations(pokerlist, 5), key=self.__m_pokerHands.jud)
        rank=self.__m_pokerHands.jud(a)
        return a, rank

    def printPoker(self):
        print('Player', self.__m_name, end=' : ')
        for pok in self.__m_pokers:
            print(pok.getDecor(), pok.getPoint(), sep='', end=' ')
        print()

    def smartBet1(self):
        suit=set()
        number=[]
        for pok in self.__m_pokers:
            suit.add(pok.getDecor())
            number.append(int(pok.getPoint()))
        real =[14 if i == 1 else i for i in number]
        if len(suit)==1 or max(real)-min(real)==1 or max(real)-min(real)==0:
            return 2
        else:
            return 1
    def smartBet2(self,rank,mbet):
        if mbet==3 and rank<2:
            return 1
        elif mbet==2 and rank <5:
            return 1
        else:
            if rank<=9 and rank>5:
                return 1
            elif rank<=5 and rank>2:
                return 2
            elif rank<=2 and rank>=0 :
                return 3
    def smartBet3(self,rank,mbet,community):
        pokerlist=self.__m_pokers + community
        plist=poker.creatPokerSet()
        elpoker = [x for x in plist if x not in pokerlist]
        ranklist=[]
        for i in itertools.combinations(elpoker, 2):
            polist=list(i)+community
            a=min(itertools.combinations(polist, 5), key=self.__m_pokerHands.jud)
            ranklist.append(self.__m_pokerHands.jud(a))
        rankdict=Counter(ranklist)
        highrank=0
        totalrank=0
        for key,value in rankdict.items():
            totalrank+=value
            if int(key) > rank:
                highrank+=value
        if highrank/totalrank <=0.5:
            if mbet == 3 and rank < 2:
                return 1
            elif mbet == 2 and rank < 5:
                return 1
            else:
                if rank <= 9 and rank > 5:
                    return 1
                elif rank <= 5 and rank > 2:
                    return 2
                elif rank <= 2 and rank >= 0:
                    return 3
        else:
            return 1



class poker:
    #poker class to store the information about every card and create a deck of cards
    def __init__(self, decor: str, value: int):
        self.__m_decor = decor
        self.__m_value = value
        self.__m_point = str(value)

    def getDecor(self) -> str:
        return self.__m_decor

    def getValue(self) -> int:
        return self.__m_value

    def getPoint(self) -> str:
        return self.__m_point

    @staticmethod
    def creatPokerSet():
        pokerSet = []
        for i in range(1, 14):
            pokerSet.append(poker('C', i))
            pokerSet.append(poker('D', i))
            pokerSet.append(poker('H', i))
            pokerSet.append(poker('S', i))

        return pokerSet

class pokerHands:
    def __init__(self):
        pass

    def getPokerHandsType(self, pokerlist : list) :
        print(' 获取牌型 还没做')
        return pokerHandsType.HIGH_CARD

    def jud(self, pokerlist : list):
        # Determining the card type, the winner has the lowest rank.
        suit = []
        number = []
        for i in pokerlist:
            suit.append(i.getDecor())
            number.append(i.getValue())
        slen = len(set(suit))
        nlen = len(set(number))
        ndict = {}
        for key in number:
            ndict[key] = ndict.get(key, 0) + 1
        dif = max(ndict.values()) - min(ndict.values())
        if slen == 1 and sorted(number) == [1, 10, 11, 12, 13]:
            return 0
        elif slen == 1 and nlen == 5 and max(number) - min(number) == 4 and min(number) != 1:
            return 1
        elif nlen == 2 and dif == 3:
            return 2
        elif nlen == 2 and dif == 1:
            return 3
        elif slen == 1:
            return 4
        elif nlen == 5 and int(max(number)) - int(min(number)) == 4 or sorted(number) == [1, 10, 11, 12, 13]:
            return 5
        elif nlen == 3 and dif == 2:
            return 6
        elif nlen == 3 and dif == 1:
            return 7
        elif nlen == 4 and dif == 1:
            return 8
        else:
            return 9
class pokerHandsType(Enum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIRS = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULLHOUSE = 7
    FOUR_OF_A_KIND = 8
    ROYAL_FLUSH = 9

if __name__ == '__main__':
    # def functionName(level):
    #     #Raise an non-number input error
    #     if level < 0:
    #         raise Exception('Please input a number more than 0.')
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', action="store_true",
                        help='Stop the game')
    parser.add_argument('-f', action="store_true",
                        help='Stop the game')
    parser.add_argument('-p', type=int, default=0,
                        help='Bot players ')
    parser.add_argument('-i', type=str, default=0,
                        help='Bot players ')

    args = parser.parse_args()

    def functionName(level):
        # Raise an non-number input error
        if level <= 0:
            raise Exception("Invalid Input")
    #print(args.f)
    if args.u:
        n_player = args.p
        cardTable().set_up_table(n_player)
    ''' try:
            #print(n_player)
            functionName(n_player)
            print(n_player)
            cardTable().set_up_table(n_player)
        except:
            print('error.')

    elif args.f:
        file_fold = args.i
        a=main(file_fold)
        print('Pass test number:',a)'''
