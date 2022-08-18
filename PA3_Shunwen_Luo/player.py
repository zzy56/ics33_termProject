from enum import Enum
import itertools
import random
from pokerHands import pokerHands


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
