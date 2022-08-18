from pokerHandsType import pokerHandsType

class pokerHands:
    def __init__(self):
        pass

    def getPokerHandsType(self, pokerlist : list) -> pokerHandsType:
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

