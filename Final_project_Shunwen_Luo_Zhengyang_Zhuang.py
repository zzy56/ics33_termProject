import argparse
from enum import Enum
import argparse
import itertools
import random
from collections import defaultdict,Counter

import tkinter as tk
from tkinter import *

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
            app.displayText(0, "1.Continue(Please enter 1)\n2.Exit (Please enter 2)\n:")
            while(app.entry.get().isnumeric() == False):
                app.button.wait_variable(app.confirmed)
                try:
                    int(app.entry.get())
                    if(int(app.entry.get()) != 1 or int(app.entry.get()) != 2):
                        continue
                    flag = int(app.entry.get())
                except:
                    continue
            app.entry.delete(0, END)

            if flag == 2:
                return
            for i in range(5):
                app.displayText(i, "\n")

    def gameStart(self):
        # main game function
        self.deal()


        for mplayer in self.__m_currentPlayers.copy():
            # mplayer.printPoker()
            if mplayer.getplayerType() == playerType.human:

                mplayer.printPoker()


        for mplayer in self.__m_currentPlayers.copy():
            if mplayer.getplayerType() == playerType.human:
                self.playerOperation(mplayer)


        str1 = ""
        for mplayer in self.__m_currentPlayers.copy():

            if mplayer.getplayerType() != playerType.human:

                bet1 = mplayer.smartBet1()
                mplayer.addbet(bet1)
                str1 += 'Player' + mplayer.getName() + ':bet $' + str(bet1) + "\n"

        app.displayText(1, str1)

        self.addCommunityCard(3)
        self.printCommunityCard()

        for mplayer in self.__m_currentPlayers.copy():
            if mplayer.getplayerType() == playerType.human:
                self.playerOperation(mplayer)

        str2 = ""
        for mplayer in self.__m_currentPlayers.copy():

            mplayer.__m_pokers, mplayer.__m_rank = mplayer.discardPoker(self.communityCard)

            if mplayer.getplayerType() != playerType.human:
                bet2=mplayer.smartBet2(mplayer.__m_rank,self.maxbet)
                mplayer.addbet(bet2)
                if self.maxbet<bet2:
                    self.maxbet=bet2
                str2 += 'Player' + mplayer.getName() + ': bet $' + str(bet2) + "\n"

        app.displayText(1, str2)


        self.addCommunityCard(2)
        self.printCommunityCard()

        for mplayer in self.__m_currentPlayers.copy():
            if mplayer.getplayerType() == playerType.human:
                self.playerOperation(mplayer)

        str3 = ""
        for mplayer in self.__m_currentPlayers.copy():
            mplayer.__m_pokers, mplayer.__m_rank = mplayer.discardPoker(self.communityCard)
            if mplayer.getplayerType() != playerType.human:
                if mplayer.__m_rank==9:
                    self.__m_currentPlayers.remove(mplayer)
                else:
                    bet3 = mplayer.smartBet3(mplayer.__m_rank, self.maxbet,self.communityCard)
                    mplayer.addbet(bet3)
                    if self.maxbet < bet3:
                        self.maxbet = bet3
                    str3 += 'Player' + mplayer.getName() + ': bet $' + str(bet3) + "\n"
        app.displayText(1, str3)


        self.judgingTiebreakers()

        winlist = [i.getName() for i in self.winners]
        totalbet = 0
        for mplayer in self.__m_allPlayers.copy():  # calculate for money
            totalbet += int(mplayer.getbet())

        for mplayer in self.__m_currentPlayers.copy():  # calculate for money
            if len(winlist) == len(self.__m_currentPlayers):
                break
            elif mplayer.getName() in winlist:
                mplayer.addMoney(totalbet / len(self.winners))
                mplayer.loseMoney(mplayer.getbet())
            else:
                mplayer.loseMoney(mplayer.getbet())

        string = ""
        string += "??????????????????Results????????????????????????\n"
        string += 'Winner: Player' + ','.join(winlist) + "\n"
        
        for mplayer in self.__m_allPlayers.copy():
            string += "Player" + mplayer.getName() + ":$" + str(mplayer.getMoney()) + "\n"
            if mplayer.getMoney() <= 0:  # if someone's lose all money, remove from game
                self.__m_allPlayers.remove(mplayer)
        app.displayText(2, string)

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
        string = ""
        string += "Community card :"
        for pok in self.communityCard:
            string += pok.getDecor() + pok.getPoint() + ' '
        string += "\n"
        app.displayText(3, string)


    def playerOperation(self, mplayer):

        type = mplayer.operation()
        if type == operationType.Discard:
            self.__m_currentPlayers.remove(mplayer)
        elif type == operationType.Filling:
            app.displayText(0, "How much you want to bet \n (please enter a number):")
            while(app.entry.get().isnumeric() == False):
                app.button.wait_variable(app.confirmed)
                try:
                    int(app.entry.get())
                    if(int(app.entry.get()) <= 0):
                        continue
                    a = int(app.entry.get())
                except:
                    continue
            a = app.entry.get()
            app.entry.delete(0, END)
            mplayer.addbet(int(a))


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
                    app.displayText(0, "Please choose your option:\n1.fold(enter 1)\n2.bet (enter 2)\n")
                    while(app.entry.get().isnumeric() == False):
                        app.button.wait_variable(app.confirmed)
                        try:
                            int(app.entry.get())
                            if(int(app.entry.get()) != 1 or int(app.entry.get()) != 2):
                                continue
                            num = int(app.entry.get())
                        except:
                            continue
                    num = int(app.entry.get())
                    app.entry.delete(0, END)
                    #num = int(input("Please choose your option:\n1.fold(enter 1)\n2.bet (enter 2)\n"))
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
        string = ""
        string += 'Player' + self.__m_name + ' : '
        for pok in self.__m_pokers:
            string += pok.getDecor() + pok.getPoint() + ' '
        string += "\n"
        app.displayText(4, string)

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
        print(' ???????????? ?????????')
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

class Gui(tk.Tk):

    def __init__(self, width, height):
        super().__init__()
        self.title('ICS33 Term Project')
        self.geometry(str(width)+"x"+str(height))
        self.entry = Entry(self, width = 20)
        self.entry.grid(row = 5, column = 0, sticky = W, pady = 2)

        self.func = None

        self.confirmed = tk.IntVar()
        self.button = tk.Button(self, text="Confirm", command=self.setConfirm)
        self.button.grid(row = 6, column = 0, sticky = W, pady = 2)

        self.startButton = tk.Button(self, text="Start", command=self.start)
        self.startButton.grid(row = 7, column = 0, sticky = W, pady = 2)

        self.labels = []
        for i in range(5):
            newLabel = Label(self, text="\n")
            newLabel.grid(row = i, column = 0, sticky = W, pady = 2)
            self.labels.append(newLabel)
        
        self.displayText(0, "Please enter the number of bot players \n you wish to have in this game (maxium 6 players), \n then press start")        
    
    def mainFunction(self, func, n_players):
        func(n_players)
        return

    def setConfirm(self, event=None):
        self.confirmed.set(-self.confirmed.get())

    def start(self):
        n_players = self.entry.get()
        try:
            int(n_players)
            if(int(n_players) > 6):
                self.displayText(1, "too many players (max 6)")
                return
            if(int(n_players) < 0):
                self.displayText(1, "there can't be negative number of players (max 6)")
                return
            if(int(n_players) == 0):
                self.displayText(1, "you can't play with yourself")
                return
        except:
            self.displayText(1, "invaild input")
            self.entry.delete(0, END)
            return

        self.startButton.destroy()
        self.entry.delete(0, END)
        self.displayText(1, "")
        self.mainFunction(self.func, int(n_players))
        self.destroy()
        return

    def displayText(self, index, text):
        self.labels[index].config(text=str(text))
        return

    def onClosing(self):
        self.confirmed.set(1)
        self.destroy()



if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    args = parser.parse_args()

    def functionName(level):
        # Raise an non-number input error
        if level <= 0:
            raise Exception("Invalid Input")
    app = Gui(400, 400)
    cT = cardTable()
    app.func = cT.set_up_table
    app.protocol("WM_DELETE_WINDOW", app.onClosing)
    app.mainloop()
