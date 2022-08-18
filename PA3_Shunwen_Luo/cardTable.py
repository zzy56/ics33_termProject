import tie_breaker
from poker import poker
from player import player
from player import operationType
from player import playerType
from dealer import dealer
from enum import Enum

class cardTable:
    def __init__(self):
        self.m_dealer = dealer() #call dealer class
        self.__m_allPlayers = []
        self.__m_currentPlayers = []
        self.pokers = poker.creatPokerSet()
        self.communityCard = []
        self.winners=[]

    def set_up_table(self, num):
        #Setting up the game environment
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
                    if mplayer.getMoney==0:
                        return
            flag = int(input("1.Continue(Please enter 1)\n2.Exit (Please enter 2)\n:"))
            if flag == 2:
                return

    def gameStart(self):
        # main game function
        print('-----Game Start-----')
        self.deal()

        print('----- Round 1 -----') # round 1


        for mplayer in self.__m_currentPlayers.copy():
            #mplayer.printPoker()
            if mplayer.getplayerType() == playerType.human:
                #print('Player', mplayer.getName(), ': rank', mplayer.__m_rank, 'bet $1')
                mplayer.printPoker()

        '''for mplayer in self.__m_currentPlayers.copy():
            #mplayer.printPoker()
            if mplayer.getplayerType() == playerType.human:
                mplayer.printPoker()
                al,mplayer.__m_rank = mplayer.discardPoker(self.communityCard)'''
                #print('Player',mplayer.getName(),': rank', mplayer.__m_rank, 'bet $1')


        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        for mplayer in self.__m_currentPlayers.copy():
            if mplayer.getplayerType() == playerType.human:
                self.playerOperation(mplayer) #p

        self.addCommunityCard(3)
        self.printCommunityCard() #p

        for mplayer in self.__m_currentPlayers.copy():
            #mplayer.printPoker()
            if mplayer.getplayerType() != playerType.human:
                print('Player', mplayer.getName(), ':bet $1') #p
                mplayer.addbet(1)
                #print(mplayer.getbet())

        print('----- Round 2 -----') #round 2


        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        for mplayer in self.__m_currentPlayers.copy():
            if mplayer.getplayerType() == playerType.human:
                self.playerOperation(mplayer) #p

        self.addCommunityCard(2)
        self.printCommunityCard() #p

        for mplayer in self.__m_currentPlayers.copy():
            #mplayer.printPoker()
            mplayer.__m_pokers,mplayer.__m_rank = mplayer.discardPoker(self.communityCard)
            #print('Player', mplayer.getName(), ': bet $1')
            if mplayer.getplayerType() != playerType.human:
                print('Player', mplayer.getName(), ': bet $1')
                mplayer.addbet(1)
                #print(mplayer.getbet())

        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        for mplayer in self.__m_currentPlayers.copy():
            if mplayer.getplayerType() == playerType.human:
                self.playerOperation(mplayer)

        for mplayer in self.__m_currentPlayers.copy():
            #mplayer.printPoker()
            mplayer.__m_pokers,mplayer.__m_rank = mplayer.discardPoker(self.communityCard)
            #print('Player', mplayer.getName(), ': bet $1')
            if mplayer.getplayerType() != playerType.human:
                print('Player', mplayer.getName(), ': bet $1')
                mplayer.addbet(1)

        self.judgingTiebreakers()

        winlist=[i.getName() for i in self.winners]
        totalbet=0
        for mplayer in self.__m_allPlayers.copy(): #calculate for money
            totalbet+=int(mplayer.getbet())
        #print(totalbet)

        for mplayer in self.__m_currentPlayers.copy():  # calculate for money
            if len(winlist)==len(self.__m_currentPlayers):
                break
            elif mplayer.getName() in winlist:
                mplayer.addMoney(totalbet/len(self.winners))
                mplayer.loseMoney(mplayer.getbet())
            else:
                mplayer.loseMoney(mplayer.getbet())

        print("——————Results————————")
        print('Winner: Player',','.join(winlist))
        for mplayer in self.__m_allPlayers.copy():
            print("Player",mplayer.getName(),":$", mplayer.getMoney())
            if mplayer.getMoney()<=0:   # if someone's lose all money, remove from game
                print("Player",mplayer.getName(),"run out of money and is removed from the game.")
                self.__m_allPlayers.remove(mplayer)
        print("——————End of Game———————— ")


    def judgingTiebreakers(self):
        best_rank = min(self.__m_currentPlayers.copy(), key=lambda poker: poker.__m_rank)
        for mplayer in self.__m_currentPlayers.copy():
            if mplayer.__m_rank==best_rank.__m_rank:
                self.winners.append(mplayer)
        wdict={}
        for i in self.winners:
            wdict[i.getName()]=i.getHandCards()

        # Judging Tiebreakers
        if best_rank == 0:
            self.winners= tie_breaker.rank0(wdict)
        elif best_rank == 1:
            self.winners= tie_breaker.rank1(wdict)
        elif best_rank == 2:
            self.winners= tie_breaker.rank2(wdict)
        elif best_rank == 3:
            self.winners= tie_breaker.rank3(wdict)
        elif best_rank == 4:
            self.winners= tie_breaker.rank4(wdict)
        elif best_rank == 5:
            self.winners= tie_breaker.rank5(wdict)
        elif best_rank == 6:
            self.winners= tie_breaker.rank6(wdict)
        elif best_rank == 7:
            self.winners= tie_breaker.rank7(wdict)
        elif best_rank == 8:
            self.winners= tie_breaker.rank8(wdict)
        elif best_rank == 9:
            self.winners= tie_breaker.rank9(wdict)

    def refreshCurrentPlayers(self):
        self.__m_currentPlayers.clear()
        for mplayer in self.__m_allPlayers:
            if mplayer.getMoney() > 0:
                self.__m_currentPlayers = self.__m_allPlayers.copy()

    def printCommunityCard(self):
        #print community card
        print("Community card :")
        for pok in self.communityCard:
            print(pok.getDecor(), pok.getPoint(), sep='', end=' ')
        print()

    def playerOperation(self,mplayer :player): 
  
        type = mplayer.operation()
        if type == operationType.Discard:
            self.__m_currentPlayers.remove(mplayer)
            print(mplayer.getName(),': fold')
        elif type == operationType.Filling:
            print(mplayer.getName(),': add bet')
            a=input("How much you want to bet:")
            mplayer.addbet(a)
        #elif type == operationType.Pass:
          #  print(mplayer.getName(),': 过牌')
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            

    def addCommunityCard(self, count: int):
        # add community card
        for i in range(count):
            self.communityCard.append(self.pokers.pop(0))

    def getPoker(self, pok: poker):
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
