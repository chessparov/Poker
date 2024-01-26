import numpy as np
import Poker_TCard
import Poker_Exceptions
from collections import defaultdict

class TDeck:
    """

    This class defines the standard Texas Hold'em 52 cards deck. Cards are disposed in a 4x13 matrix
    with all cards with the same suit in a row. Row order is:
    1st row -> Spades
    2nd row -> Hearts
    3rd row -> Diamonds
    4th row -> Clubs
    As for formatting:
    Accepted values are 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K, A.
    Accepted suits are h -> Hearts, s -> Spades, c -> Clubs, d -> Diamonds

    """

    def __init__(self):
        lstValues = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        lstSuits = ['S', 'H', 'D', 'C']
        self._suits = lstSuits
        self._values = lstValues
        self.__deckname = 'Deck'
        self._cards = np.zeros((4, 13), dtype=object)
        self._cardnames = np.zeros((4, 13), dtype=object)
        self._cardsnumber = np.count_nonzero(self.getCards())

    def setdeckName(self, name: str):
        self.__deckname = name

    def getdeckName(self):
        return self.__deckname

    # Allows to add a card in your deck and performs checks upon the validity of the given card
    def addCard(self, card: Poker_TCard.TCard):
        if card.getValue() in self._values:
            value = card.getValue()
            col = self._values.index(value)
        else:
            raise Poker_Exceptions.InvalidCard
        if card.getSuit() in self._suits:
            suit = card.getSuit()
            row = self._suits.index(suit)
        else:
            raise Poker_Exceptions.ExceptInvalidCard
        if self._cards[row, col] == 0:
            self._cards[row, col] = card
            self._cardnames[row, col] = card.getName()
        else:
            raise Poker_Exceptions.ExceptCardExist

    # Allows to remove a given card in the form of a TCard, and updates the deck.
    def removeCard(self, card: Poker_TCard.TCard):
        if card.getName() in self._cardnames:
            suit = card.getSuit()
            value = card.getValue()
            col = self._values.index(value)
            row = self._suits.index(suit)
            self._cards[row, col] = 0
            self._cardnames[self._cardnames == card.getName()] = 0
        else:
            print(f"\nCard already doesn't exist. "
                  f"Are you sure {card.getName()} is the right card to remove?\n")

    def getCards(self):
        """

        Returns the list of cards (object TCard) in a "np.array" 4x13 currently in the deck

        """
        return self._cards

    def getCardNames(self):
        return self._cardnames

    # Returns the current number of cards in the deck
    def getCardsNumber(self):
        return self._cardsnumber

    # From the current cards in the deck, extrapolates only the values
    # Double version, dictionary or list. I'll decide later which one is more useful.
    def getDeckValues(self):
        # lstCurrentVal = []
        dctCurrentVal = defaultdict(int)
        for i, row in enumerate(self.getCards()):
            for j, card in enumerate(row):
                if card != 0:
                    value = card.getValue()
                    # lstCurrentVal.append(value)
                    dctCurrentVal[value] += 1
        # return lstCurrentVal
        return dctCurrentVal

    # From the current cards in the deck, extrapolates only the suits
    # Same as above, uncomment for alternative version
    def getDeckSuits(self):
        # lstCurrentSuits = []
        dctCurrentSuits = defaultdict(int)
        for i, row in enumerate(self.getCards()):
            for j, card in enumerate(row):
                if card != 0:
                    suit = card.getSuit()
                    dctCurrentSuits[suit] += 1
                    # lstCurrentSuits.append(suit)
        # return lstCurrentSuits
        return dctCurrentSuits

    def getValues(self):
        return self._values

    def getSuits(self):
        return self._suits
