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