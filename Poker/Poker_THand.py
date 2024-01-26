import Poker_Exceptions
import Poker_TCard
import Poker_TDeck
import Poker_TStdDeck
import copy

class THand:
    """

    Simulates a Texas Hold'em hand => 2 hole cards and 5 common cards distributed afterwards in 3 rounds:
    Flop, Turn and River. Not accounting pot odds for the moment, but soon it will.

    """

    def __init__(self, deck: Poker_TDeck.TDeck, players: int):
        if isinstance(deck, Poker_TDeck.TDeck):
            self.deck = deck
        else:
            raise Poker_Exceptions.ExceptInvalidDeck
        if isinstance(players, int):
            if players > 0:
                self.__players = players

        self.__pot = int(0)
        self.table = list()
        self.hand = list()
        self.pocket = list()
        self.deckcopy = copy.deepcopy(self.deck)
        self._greenthreshold = float(0.10)      # Used as parameters in termcolor to color in certain ways different percentages
        self._redthreshold = float(0.30)

    # Same as for the other getCards: returns the cards in your hand (getHand) and the common cards (getTable)
    def getPocket(self):
        return self.pocket

    def getTable(self):
        return self.table

    def getCurrentDeckCards(self):
        return self.deckcopy.getCards()

    def getCurrentDeckCardNames(self):
        return self.deckcopy.getCardNames()

    def getCurrentDeckCardNumber(self):
        pass

    def getPot(self):
        return self.__pot

    def setGreen(self, threshold: float):
        """
        Use a number between 0 and 1, all probabilities (regarding your hand) above this threshold will be set to green
        and therefore printed accordingly on terminal
        """
        if 0 < threshold < 1:
            self._greenthreshold = threshold
        else:
            raise ValueError

    def getGreen(self):
        return self._greenthreshold

    def setRed(self, threshold: float):
        """
        Use a number between 0 and 1, all probabilities (regarding your opponents hand) above this threshold will be set to red
        and therefore printed accordingly on terminal
        """
        if 0 < threshold < 1:
            self._redthreshold = threshold
        else:
            raise ValueError

    def getRed(self):
        return self._redthreshold

    def getHand(self):
        return self.hand

    def getHandNames(self):
        lstNames = []
        for card in self.getHand():
            lstNames.append(card.getName())
        return lstNames
    # Useful for getting a printable from a TCard list
    def getNamesMap(self, lst: list):
        return list(map(Poker_TCard.TCard.getName, lst))

    def getValuesMap(self, lst: list):
        return list(map(Poker_TCard.TCard.getValue, lst))

    def orderHand(self):
        pass

    def getDeck(self):
        return self.deck
