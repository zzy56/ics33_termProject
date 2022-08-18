import random 
from pokerHands import pokerHands

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
