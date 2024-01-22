"""

The scope of the following code is to analyze in real time a poker game (valid only fo Texas Hold'em rules). The classes and methods defined below offer help in calculating the odds and the hands
given the user's input.

"""
import numpy as np
from collections import defaultdict
import copy
# import scipy as sp                        # Used for sp.special.binom
from termcolor import colored
import sys
import colorama
import time

# Import sys for trying to solve termcolor package malfunction
# sys.path.append('/home/cristian/PycharmProjects/venv/MainDir/lib/python3.11/site-packages/')

class ExceptInvalidCard(Exception):
    """
    Class ExceptInvalidCard

    Occurs if the value or the suit aren't amongst the accepted ones.

    """

    def __init__(self, *args):
        super().__init__(self, *args)

    def __str__(self):
        return f"Please insert a valid card!"

class ExceptInvalidHand(Exception):
    """
    Class ExceptInvalidHand

    Occurs if the cards in a hand are the same card or if other formatting error has been made in a hand declaration.

    """

    def __init__(self, *args):
        super().__init__(self, *args)

    def __str__(self):
        return f"Please ensure your hands is made of valid cards!"


class ExceptInvalidCardLenght(Exception):
    """
    Class ExceptInvalidCard

    Occurs either if the card's name is not properly formatted or if the string contains a different amount of characters than expected.

    """

    def __init__(self, *args):
        super().__init__(self, *args)

    def __str__(self):
        return (f"Please insert a valid card! "
                f"With the sole exception of '10h', '10c', '10s' and '10d', the name should contain exactly two characters. ")

class ExceptInvalidDeck(Exception):
    """
    Class ExceptInvalidDeck

    Occurs if you pass an object different from a deck.

    """

    def __init__(self, *args):
        super().__init__(self, *args)

    def __str__(self):
        return f"Please insert a valid deck! "

class ExceptCardExist(Exception):
    """
    Class ExceptCardExist

    Occurs if the card you're trying to add to a deck is already existent.

    """

    def __init__(self, *args):
        super().__init__(self, *args)

    def __str__(self):
        return f"Card already exist! You cannot have duplicates of the same card in a standard deck! "


class TCard:
    """

    The card name should be formatted 'value + suit' without space in between like in this example 'Jh'.
    You can both use lowercase or uppercase characters, all strings are treated as uppercase
    regardless the user input.
    ------------------------------------------------------------------------
    Accepted values are 2, 3, 4, 5, 6, 7, 8, 9, 10 (also T), J, Q, K, A.
    Accepted suits are h -> Hearts, s -> Spades, c -> Clubs, d -> Diamonds
    ------------------------------------------------------------------------
    A small note about the value "10": both "10" and "T" are valid inputs, but "10" is immediately
    converted to "T", in order to have all card names as a string made of 2 characters.
    Expect all outputs to have "T" in place of "10" regardless of the input.

    """
    def __init__(self, strName: str):
        super().__init__()
        self._name = strName.upper()
        if len(strName) != 2:
            if strName[0:2] == '10':
                self._value = 'T'
                self._suit = strName[2].upper()
                self._name = ''.join([self._value, self._suit])
                self.__printable_name = strName
            else:
                raise ExceptInvalidCardLenght
        else:
            self._value = strName[0].upper()
            self._suit = strName[1].upper()

    def __del__(self):
        self.__printable_name = ''
        self._name = ''
        self._value = ''
        self._suit = ''

    def getName(self):
        return self._name
    def getValue(self):
        return self._value
    def getSuit(self):
        return self._suit

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
    def addCard(self, card: TCard):
        if card.getValue() in self._values:
            value = card.getValue()
            col = self._values.index(value)
        else:
            raise ExceptInvalidCard
        if card.getSuit() in self._suits:
            suit = card.getSuit()
            row = self._suits.index(suit)
        else:
            raise ExceptInvalidCard
        if self._cards[row, col] == 0:
            self._cards[row, col] = card
            self._cardnames[row, col] = card.getName()
        else:
            raise ExceptCardExist

    # Allows to remove a given card in the form of a TCard, and updates the deck.
    def removeCard(self, card: TCard):
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

class TStdDeck(TDeck):
    """
    An untouched and complete Texas Hold'em deck containing all 52 cards.

    """
    def __init__(self):
        super().__init__()
        card_matrix = list()
        card_names_matrix = list()
        for suit in self._suits:
            for value in self._values:
                new_card_name = ''.join([value, suit])
                new_card = TCard(new_card_name)
                card_matrix.append(new_card)
                card_names_matrix.append(new_card_name)
        card_matrix = np.reshape(card_matrix, (4, 13))
        card_names_matrix = np.reshape(card_names_matrix, (4, 13))
        self._cardnames = np.array(card_names_matrix, dtype=str)
        self._cards = np.array(card_matrix, dtype=TCard)
        self._cardsnumber = 52


class THand:
    """

    Simulates a Texas Hold'em hand => 2 hole cards and 5 common cards distributed afterwards in 3 rounds:
    Flop, Turn and River. Not accounting pot odds for the moment, but soon it will.

    """

    def __init__(self, deck: TDeck, players: int):
        if isinstance(deck, TDeck):
            self.__deck = deck
        else:
            raise ExceptInvalidDeck
        if isinstance(players, int):
            if players > 0:
                self.__players = players
        self.__table = list()
        self._hand = list()
        self.__deckcopy = copy.deepcopy(self.__deck)
        self._greenthreshold = float(0.10)      # Used as parameters in termcolor to color in certain ways different percentages
        self._redthreshold = float(0.30)
        colorama.init()

        ################################################################################################################
        # PreFlop
        ################################################################################################################

        user_input = str

        while True:
            try:
                user_input = input('\nFor info about how to format the input of cards, type "help" (then press "q" to terminate'
                                   ' the help function);  otherwise, press enter: ').lower()
                if user_input == 'help':
                    help(TCard)
                    break
                elif user_input == '':
                    break
                else:
                    raise Exception
            except:
                print(f'\n"{user_input}"'f" it's not a valid input! Please try again. ")

        card1 = TCard(input(f'\nInsert your first card (e.g. "jh"): '))
        card2 = TCard(input(f'Insert your second card (e.g. "jh"): '))
        # card1 = TCard('2h')       # Made for testing purposes
        # card2 = TCard('9h')       # Comment the above and de-comment those two for additional testing
        if card1.getName() in self.__deck.getCardNames():
            if card1.getName() in self.__deckcopy.getCardNames():
                self.__card1 = card1
                self.__deckcopy.removeCard(card1)
                self._hand.append(self.__card1)
            else:
                raise ExceptCardExist
        else:
            raise ExceptInvalidCard
        if card2.getName() in self.__deck.getCardNames():
            if card2.getName() in self.__deckcopy.getCardNames():
                self.__card2 = card2
                self.__deckcopy.removeCard(card2)
                self._hand.append(self.__card2)
            else:
                raise ExceptCardExist
        else:
            raise ExceptInvalidCard

        print(f'\n{"":45s}{"Current Hand":25s}{"Pocket":20s}{"Table":25s}')
        print(f'{self.what_do_I_have():35s}\n')
        print(f'The probabilities of improving your hand in the flop are:\n')
        print(f'{"":33s}{"Probability":20s}\t{"Odds":10s}')

        # All the following if statements have tho only purpose to change the print color of the probability,
        # if it's above a threshold (default = 10%)

        if self.pair_preflop() > self._greenthreshold:
            print(colored(f'{"Pair: ":33s}{self.pair_preflop():<10.3%}\t\t{"1:"}{(1 / self.pair_preflop()) - 1:<.2f}', "green"))
        else:
            print(f'{"Pair: ":33s}{self.pair_preflop():<10.3%}\t\t{"1:"}{(1/self.pair_preflop()) - 1:<.2f}')
        if self.dpair_preflop() > self._greenthreshold:
            print(colored(f'{"Double Pair: ":33s}{self.dpair_preflop():<10.3%}\t\t{"1:"}{(1/self.dpair_preflop()) - 1:<.2f}', 'green'))
        else:
            print(f'{"Double Pair: ":33s}{self.dpair_preflop():<10.3%}\t\t{"1:"}{(1/self.dpair_preflop()) - 1:<.2f}')
        if self.dpair_preflop_table() > self._greenthreshold:
            print(colored(f'{"Double Pair & table pair: ":33s}{self.dpair_preflop_table():<10.3%}\t\t{"1:"}{(1/self.dpair_preflop_table()) - 1:<.2f}',
                          'green'))
        else:
            print(f'{"Double Pair & table pair: ":33s}{self.dpair_preflop_table():<10.3%}\t\t{"1:"}{(1/self.dpair_preflop_table()) - 1:<.2f}')

        # Not gonna check for probability above 10% cause is obviously pointless

        print(f'{"Three of a kind:":33s}{self.three_preflop():<10.3%}\t\t{"1:"}{(1/self.three_preflop()) - 1:<.2f}')
        print(f'{"Straight:":33s}{self.straight_preflop():<10.3%}\t\t{"1:"}{(1 / self.straight_preflop()) - 1:<.2f}')
        print(f'{"Flush:":33s}{self.flush_preflop():<10.3%}\t\t{"1:"}{(1 / self.flush_preflop()) - 1:<.2f}')
        print(f'{"Full house:":33s}{self.full_preflop():<10.3%}\t\t{"1:"}{(1 / self.full_preflop()) - 1:<.2f}')
        print(f'{"Four of a kind:":33s}{self.four_preflop():<10.3%}\t\t{"1:"}{(1 / self.four_preflop()) - 1:<.0f}')
        print(f'{"Straight flush:":33s}{self.straightflush_preflop():<10.3%}\t\t{"1:"}{(1 / self.straightflush_preflop()) - 1:<.2f}')
        print(f'{"Royal flush:":33s}{self.royalflush_preflop():<10.3%}\t\t{"1:"}{(1 / self.royalflush_preflop()) - 1:<.2f}\n')

        ################################################################################################################
        # Flop (Pre-turn)
        ################################################################################################################

        card3 = TCard(input(f'Insert the first flop card (e.g. "jh"): '))
        card4 = TCard(input(f'Insert the second flop card (e.g. "jh"): '))
        card5 = TCard(input(f'Insert the third flop card (e.g. "jh"): '))
        # card3 = TCard('jh')       # Other testing cards. Keep commented till needed
        # card4 = TCard('qh')
        # card5 = TCard('ad')

        if card3.getName() not in self.__deck.getCardNames():
            raise ExceptInvalidCard
        elif card3.getName() not in self.__deckcopy.getCardNames():
            raise ExceptCardExist
        else:
            self.__card3 = card3
            self.__table.append(card3)
            self._hand.append(self.__card3)
            self.__deckcopy.removeCard(card3)
        if card4.getName() not in self.__deck.getCardNames():
            raise ExceptInvalidCard
        elif card4.getName() not in self.__deckcopy.getCardNames():
            raise ExceptCardExist
        else:
            self.__card4 = card4
            self.__table.append(card4)
            self._hand.append(self.__card4)
            self.__deckcopy.removeCard(card4)
        if card5.getName() not in self.__deck.getCardNames():
            raise ExceptInvalidCard
        elif card5.getName() not in self.__deckcopy.getCardNames():
            raise ExceptCardExist
        else:
            self.__card5 = card5
            self.__table.append(card5)
            self._hand.append(self.__card5)
            self.__deckcopy.removeCard(card5)

        print(f'\n{"":45s}{"Current Hand":25s}{"Pocket":20s}{"Table":25s}')
        print(f'{self.what_do_I_have():35s}\n')
        print(f'The probabilities of improving your hand in the turn are:\n')
        print(f'{"":33s}{"Probability":20s}\t{"Odds":10s}')

        print(f'{"Pair:":33s}{1:<10.3%}\t\t{"1:"}{(1 / 1) - 1:<.2f}')
        print(f'{"Double Pair:":33s}{1:<10.3%}\t\t{"1:"}{(1 / 1) - 1:<.2f}')
        print(f'{"Three of a kind:":33s}{1:<10.3%}\t\t{"1:"}{(1 / 1) - 1:<.2f}')
        print(f'{"Straight:":33s}{1:<10.3%}\t\t{"1:"}{(1 / 1) - 1:<.2f}')
        print(f'{"Flush:":33s}{1:<10.3%}\t\t{"1:"}{(1 / 1) - 1:<.2f}')
        print(f'{"Full house:":33s}{1:<10.3%}\t\t{"1:"}{(1 / 1) - 1:<.2f}')
        print(f'{"Four of a kind:":33s}{1:<10.3%}\t\t{"1:"}{(1 / 1) - 1:<.2f}')
        print(f'{"Straight flush:":33s}{1:<10.3%}\t\t{"1:"}{(1 / 1) - 1:<.2f}')
        print(f'{"Royal flush":33s}{1:<10.3%}\t\t{"1:"}{(1 / 1) - 1:<.2f}\n')

        #######################################################################################
        # Turn (Pre-river)
        #######################################################################################

        card6 = TCard(input(f'Insert the turn card (e.g. "jh"): '))
        # card6 = TCard('kh')       # Test card

        if card6.getName() not in self.__deck.getCardNames():
            raise ExceptInvalidCard
        elif card6.getName() not in self.__deckcopy.getCardNames():
            raise ExceptCardExist
        else:
            self.__card6 = card6
            self.__table.append(card6)
            self._hand.append(self.__card6)
            self.__deckcopy.removeCard(card6)

        print(f'\n{"":45s}{"Current Hand":25s}{"Pocket":20s}{"Table":25s}')
        print(f'{self.what_do_I_have():35s}\n')
        print(f'The probabilities of improving your hand in the river are:\n')
        print(f'{"":33s}{"Probability":20s}\t{"Odds":10s}')

        print(f'{"Pair:":33s}{1:<10.3%}\t\t{"1:"}{(1 / 1) - 1:<.2f}')
        print(f'{"Double Pair:":33s}{1:<10.3%}\t\t{"1:"}{(1 / 1) - 1:<.2f}')
        print(f'{"Three of a kind:":33s}{1:<10.3%}\t\t{"1:"}{(1 / 1) - 1:<.2f}')
        print(f'{"Straight:":33s}{1:<10.3%}\t\t{"1:"}{(1 / 1) - 1:<.2f}')
        print(f'{"Flush:":33s}{1:<10.3%}\t\t{"1:"}{(1 / 1) - 1:<.2f}')
        print(f'{"Full house:":33s}{1:<10.3%}\t\t{"1:"}{(1 / 1) - 1:<.2f}')
        print(f'{"Four of a kind:":33s}{1:<10.3%}\t\t{"1:"}{(1 / 1) - 1:<.2f}')
        print(f'{"Straight flush:":33s}{1:<10.3%}\t\t{"1:"}{(1 / 1) - 1:<.2f}')
        print(f'{"Royal flush":33s}{1:<10.3%}\t\t{"1:"}{(1 / 1) - 1:<.2f}\n')

        #######################################################################################
        # River (Last card dealt)
        #######################################################################################

        card7 = TCard(input(f'Insert the river card (e.g "jh"): '))
        # card7 = TCard('10h')        # Test Card

        if card7.getName() not in self.__deck.getCardNames():
            raise ExceptInvalidCard
        elif card7.getName() not in self.__deckcopy.getCardNames():
            raise ExceptCardExist
        else:
            self.__card7 = card7
            self.__table.append(card7)
            self._hand.append(self.__card7)
            self.__deckcopy.removeCard(card7)

        print(f'\n{"":45s}{"Current Hand":25s}{"Pocket":20s}{"Table":25s}')
        print(f'{self.what_do_I_have():35s}\n')
        print(f'The probabilities of holding the nuts (winning combination):\n')

        print(f'{"Pair:":33s}{1:<10.3%}\t\t{"1:"}{(1 / 1) - 1:<.2f}')
        print(f'{"Double Pair:":33s}{1:<10.3%}\t\t{"1:"}{(1 / 1) - 1:<.2f}')
        print(f'{"Three of a kind:":33s}{1:<10.3%}\t\t{"1:"}{(1 / 1) - 1:<.2f}')
        print(f'{"Straight:":33s}{1:<10.3%}\t\t{"1:"}{(1 / 1) - 1:<.2f}')
        print(f'{"Flush:":33s}{1:<10.3%}\t\t{"1:"}{(1 / 1) - 1:<.2f}')
        print(f'{"Full house:":33s}{1:<10.3%}\t\t{"1:"}{(1 / 1) - 1:<.2f}')
        print(f'{"Four of a kind:":33s}{1:<10.3%}\t\t{"1:"}{(1 / 1) - 1:<.2f}')
        print(f'{"Straight flush:":33s}{1:<10.3%}\t\t{"1:"}{(1 / 1) - 1:<.2f}')
        print(f'{"Royal flush":33s}{1:<10.3%}\t\t{"1:"}{(1 / 1) - 1:<.2f}\n')

    ################################################################################
    # End of constructor
    ################################################################################

    # Same as for the other getCards: returns the cards in your hand (getHand) and the common cards (getTable)
    def getPocket(self):
        return [self.__card1, self.__card2]

    def getTable(self):
        return self.__table

    def getCurrentDeckCards(self):
        return self.__deckcopy.getCards()

    def getCurrentDeckCardNames(self):
        return self.__deckcopy.getCardNames()

    def getCurrentDeckCardNumber(self):
        pass

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
        return self._hand

    def getHandNames(self):
        lstNames = []
        for card in self.getHand():
            lstNames.append(card.getName())
        return lstNames
    # Useful for getting a printable from a TCard list
    def getNamesMap(self, lst: list):
        return list(map(TCard.getName, lst))

    def getValuesMap(self, lst: list):
        return list(map(TCard.getValue, lst))

    def orderHand(self):
        pass

    def getDeck(self):
        return self.__deck

    # Prints a f-string containing information about your current hand
    def what_do_I_have(self):

        lstCards = self.getHand()
        lstValues = list(map(TCard.getValue, self.getHand()))
        lstSuits = list(map(TCard.getSuit, self.getHand()))

        # Returns the hierarchic index of a particular card
        def getIndex(value: str):
            index = self.getDeck().getValues().index(value)
            return index
        # Returns a card value given the index
        def getValfromIndx(index: int):
            return self.getDeck().getValues()[index]
        # Orders the list according to the index
        def orderValues(lst: list):
                return sorted(lst, key=lambda x: getIndex(x))
        # Gets the highest value of a list
        def getHighest(lst: list):
            lst = sorted(lst, key=lambda x: getIndex(x), reverse=True)
            return lst[0]
        # Order a lis of TCards by value. N.B. Use only for list of cards with no double values
        # otherwise an error will be raised
        def orderCards(lst: list) -> list:
            lstCards = []
            for i, card in enumerate(lst):
                index = getIndex(card.getValue())
                lstCards.append((index, card))
            lstCards.sort()
            ordered_cards = list()
            for tpl in lstCards:
                ordered_cards.append(tpl[1])
            return ordered_cards

        ######################################################################
        # Combination checks
        ######################################################################

        def checkforRoyalflush():
            royal_flush = ["T", "J", "Q", "K", "A"]
            royal = []
            j = int(0)
            if checkforStraight() and getHighest(list(map(TCard.getValue, checkforStraight()))) == 'A':
                if checkforFlush():
                    for card in checkforFlush():
                        if card.getValue() in royal_flush:
                            j += 1
                            royal.append(card)
            if j == 5:
                return royal

        def checkforStraightflush():
            if checkforFlush():
                if checkforStraight(checkforFlush()):
                    return checkforStraight(checkforFlush())

        def checkforFour():
            four = []
            for card in lstCards:
                value = card.getValue()
                if list(map(TCard.getValue, lstCards)).count(value) == 4:
                    four.append(card)
            return four

        def checkforFull():
            full = []
            highest_full = []
            three_indexes = []
            pair_indexes = []
            three_bool = int(0)
            for card in lstCards:
                value = card.getValue()
                if list(map(TCard.getValue, lstCards)).count(value) == 2:
                    full.append(card)
                    if getIndex(value) not in pair_indexes:
                        pair_indexes.append(getIndex(value))
                if list(map(TCard.getValue, lstCards)).count(value) == 3:
                    if getIndex(value) not in three_indexes:
                        three_indexes.append(getIndex(value))
                    full.append(card)
                    three_bool = 1
            three_indexes.sort(reverse=True)
            pair_indexes.sort(reverse=True)
            counter = int(0)
            if three_bool:
                if len(full) > 5:
                    if len(three_indexes) == 1:
                        for fullcard in full:
                            if getIndex(fullcard.getValue()) == three_indexes[0]:
                                highest_full.append(fullcard)
                            if getIndex(fullcard.getValue()) == pair_indexes[0]:
                                if counter < 2:
                                    highest_full.append(fullcard)
                                    counter += 1
                        return highest_full
                    elif len(three_indexes) > 1:
                        for fullcard in full:
                            if getIndex(fullcard.getValue()) == three_indexes[0]:
                                highest_full.append(fullcard)
                            if getIndex(fullcard.getValue()) == three_indexes[1]:
                                if counter < 2:
                                    highest_full.append(fullcard)
                                    counter += 1
                        return highest_full
                if len(full) == 5:
                    return full

        def checkforFlush():
            flush = []
            for suit in self.getDeck()._suits:
                if lstSuits.count(suit) >= 5:
                    for i, card in enumerate(lstCards):
                        if card.getSuit() == suit:
                            flush.append(card)
            if len(flush) > 5:
                flush = orderCards(flush)[-5:]
            return flush

        # The function thea is divided in 3 sections
        # 1° ---> Looks for a straight. Operates using the values of the TCards
        # 2° ---> Looks for a possible cross-case of a straight flush or other weird interactions with flushes
        # 3° ---> Converts back values to TCards and returns the highest 5 elements of the straight,
        # preferring the ones in pocket when the index is the same
        #
        # Default value set to list of cards currently in play (pocket + table),
        # but accepts also other lists in order to avoid checking for a possible
        # royal flush or straight flush
        def checkforStraight(lst: list = lstCards) -> list:

            straight = []                                           # The final list containing the TCards actually forming a straight
            value_straight = []                                     # The temp list containing the values of the TCards in a possible straight
            ace_first = [12, 0, 1, 2, 3]                            # The ace can both be used before a 2 or after a K
            i_list = list(map(getIndex, orderValues(lstValues)))    # The list containing all the values of the hand

            # Checks if among the valus in i_list there are consecutive values
            # and adds the to value_straight
            for i in range(0, len(i_list) - 1):
                if i_list[i] == i_list[i + 1]:
                    continue
                elif i_list[i] + 1 == i_list[i + 1]:
                    value_straight.append(i_list[i])
                else:
                    # Allows the possibility of having a straight with the ace in front
                    if value_straight[0:3] == [0, 1, 2] and i_list[i] == 3:
                        if 12 in i_list:
                            value_straight.insert(0, 12)
                            value_straight.append(i_list[i])
                            break
                        else:
                            value_straight = []             # Restart from zero, all the previous
                    elif len(value_straight) >= 4:          # elements don't belong to a straight
                        value_straight.append(i_list[i])
                        break
                    else:
                        value_straight = []
                # Last element can check anything else, but has already been checked, so it's added
                if i == len(i_list) - 2:
                    if i_list[i] in value_straight:
                        value_straight.append(i_list[i + 1])

            # This section looks after a flush
            flush_counter = int(0)
            flush = {}
            flush2 = []
            if checkforFlush():
                for card in orderCards(checkforFlush()):
                    flush_index = getIndex(card.getValue())
                    if flush_index in value_straight:
                        flush_counter += 1
                        flush[flush_index] = card
                # if there are at least 5 elements both in the straight and in the flush,
                # we check if 5 of the elements in the flush are also in the straight
                if flush_counter >= 5:
                    flush_counter2 = int(0)
                    # This part is quite similar to the one we firstly used. Might as well separate it
                    # in a dedicated function
                    for i in range(len(flush.keys()) - 1):
                        if list(flush.keys())[i] == list(flush.keys())[i + 1] - 1:
                            flush_counter2 += 1
                            flush2.append(flush[list(flush.keys())[i]])
                        elif len(flush2) >= 4:
                            flush2.append(i_list[flush[list(flush.keys())[i]]])
                            break
                        else:
                            flush2 = []
                        if i == len(flush.keys()) - 2:
                            if flush[list(flush.keys())[i]] in flush2:
                                flush2.append(flush[list(flush.keys())[i + 1]])
                    # Altough quite unlikely, we have to check if there are more than 5 items,
                    # and pick the higher ones
                    if len(flush2) > 5:
                        return flush2[-5:]
                    if len(flush2) == 5:
                        return flush2

            # If there's no flush we are safe reducing directly the domain of the straight
            if len(value_straight) > 5:
                value_straight = value_straight[-5:]
            for card in lst:
                index = getIndex(card.getValue())
                if index in value_straight:
                    if (list(map(getIndex, self.getValuesMap(lst)))).count(index) > 1:
                        # If there are more cards with the same value we pick only one
                        # Preference is given to the ones we hold, altough it doesn't really matter
                        for your_card in self.getPocket():
                            if index == getIndex(your_card.getValue()):
                                straight.append(your_card)
                                break
                        straight.append(card)
                        value_straight.remove(index)
                    else:
                        straight.append(card)
            if len(straight) == 5:
                return straight

        def checkforThree():
            three = []
            for card in lstCards:
                value = card.getValue()
                if list(map(TCard.getValue, lstCards)).count(value) == 3:
                    three.append(card)
            return three

        def checkforDPair():
            dpair = []
            dvalues = []
            highest_dpair = []
            j = int(0)
            for card in lstCards:
                value = card.getValue()
                if list(map(TCard.getValue, lstCards)).count(value) == 2:
                    dvalues.append(getIndex(value))
                    dpair.append(card)
                    j += 1
            dvalues.sort(reverse=True)
            if j == 4:
                return dpair
            elif j > 4:
                for card1 in dpair:
                    if getIndex(card1.getValue()) in dvalues[0:4]:
                        highest_dpair.append(card1)
                return highest_dpair

        def checkforPair():
            pair = []
            # Legacy version used directly the list of values, new one operates directly to the card.
            # for value in lstValues:
            #     if lstValues.count(value) == 2:
            for card in lstCards:
                if list(map(TCard.getValue, lstCards)).count(card.getValue()) == 2:
                    pair.append(card)
            return pair

        def checkforHigh():
            lstIndex = list(map(getIndex, lstValues))
            for card in lstCards:
                if getIndex(card.getValue()) == max(lstIndex):
                    high_card = card
                    return high_card

        # Check for number of cards, if below 5 -> exclude all straights and flushes, if below 4 -> exclude four of a kind
        # and double pairs, if below 3, also three of a kind
        # Check whether the flop has already come. If no, exclude all of above combinations
        pocket = self.getNamesMap(self.getPocket())
        table = self.getNamesMap(self.getTable())
        if len(lstCards) < 3:
            if lstValues[0] == lstValues[1]:
                return (f'{"You have a Pair":45s}' +
                        colored(f'{"  ".join(map(str, self.getNamesMap(checkforPair()))):25s}', color='light_yellow') +
                        f'{"  ".join(map(str, pocket)):20s}{"  ".join(map(str, table)):25s}')
            else:
                return (f'{"You have a High card":45s}' +
                        colored(f'{orderCards(self.getPocket())[1].getName():25s}', color='light_yellow') +
                        f'{"  ".join(map(str, pocket)):20s}{"  ".join(map(str, table)):25s}')
        else:
            if checkforRoyalflush():
                return (f'{"You have a Royal Flush":45s}' +
                        colored(f'{"  ".join(map(str, self.getNamesMap(checkforRoyalflush()))):25s}',
                                color='light_yellow') +
                        f'{"  ".join(map(str, pocket)):20s}{"  ".join(map(str, table)):25s}')
            elif checkforStraightflush():
                return (f'{"You have a Straight flush":45s}' +
                        colored(f'{"  ".join(map(str, self.getNamesMap(checkforStraightflush()))):25s}',
                                color='light_yellow') +
                        f'{"  ".join(map(str, pocket)):20s}{"  ".join(map(str, table)):25s}')
            elif checkforFour():
                return (f'{"You have a Four of a kind":45s}' +
                        colored(f'{"  ".join(map(str, self.getNamesMap(checkforFour()))):25s}',
                                color='light_yellow') +
                        f'{"  ".join(map(str, pocket)):20s}{"  ".join(map(str, table)):25s}')
            elif checkforFull():
                return (f'{"You have a Full house":45s}' +
                        colored(f'{"  ".join(map(str, self.getNamesMap(checkforFull()))):25s}',
                                color='light_yellow') +
                        f'{"  ".join(map(str, pocket)):20s}{"  ".join(map(str, table)):25s}')
            elif checkforFlush():
                return (f'{"You have a Flush":45s}' +
                        colored(f'{"  ".join(map(str, self.getNamesMap(checkforFlush()))):25s}',
                                color='light_yellow') +
                        f'{"  ".join(map(str, pocket)):20s}{"  ".join(map(str, table)):25s}')
            elif checkforStraight():
                return (f'{"You have a Straight":45s}' +
                        colored(f'{"  ".join(map(str, self.getNamesMap(checkforStraight()))):25s}',
                                color='light_yellow') +
                        f'{"  ".join(map(str, pocket)):20s}{"  ".join(map(str, table)):25s}')
            elif checkforThree():
                return (f'{"You have a Three of a kind":45s}' +
                        colored(f'{"  ".join(map(str, self.getNamesMap(checkforThree()))):25s}',
                                color='light_yellow') +
                        f'{"  ".join(map(str, pocket)):20s}{"  ".join(map(str, table)):25s}')
            elif checkforDPair():
                return (f'{"You have a Double Pair":45s}' +
                        colored(f'{"  ".join(map(str, self.getNamesMap(checkforDPair()))):25s}',
                                color='light_yellow') +
                        f'{"  ".join(map(str, pocket)):20s}{"  ".join(map(str, table)):25s}')
            elif checkforPair():
                return (f'{"You have a Pair":45s}' +
                        colored(f'{"  ".join(map(str, self.getNamesMap(checkforPair()))):25s}'
                                , color='light_yellow') +
                        f'{"  ".join(map(str, pocket)):20s}'
                        f'{"  ".join(map(str, table)):25s}')
            else:

                return (f'{"You have a High card":45s}' +
                        colored(f'{orderCards(self.getPocket())[1].getName():25s}', color='light_yellow') +
                        f'{"  ".join(map(str, pocket)):20s}{"  ".join(map(str, table)):25s}')

    ###########################################################################################
    # Probabilities of improving on the flop. Calculated pre-flop, thus the names
    ###########################################################################################

    # N.B. All of the following probabilities are calculated excluding the possibility of getting an even better hand,
    # thus not contaminating the odds. Sometimes the cumulative odds can be useful, but those are left to dedicated functions.

    # Returns the probability of getting a pair before the turn
    def pair_preflop(self):
        card1 = self.__card1
        card2 = self.__card2
        val1 = card1.getValue()
        val2 = card2.getValue()
        if val1 == val2:
            return 1
        else:
            return (6/50) + (44/50)*(6/49) + (44/50)*(43/49)*(6/48)

    # Returns the probability of getting a double pair before the turn
    def dpair_preflop_table(self):
        card1 = self.__card1
        card2 = self.__card2
        val1 = card1.getValue()
        val2 = card2.getValue()
        if val1 == val2:
            return (48/50)*(3/49) + (48/50)*(44/49)*(3/48)
        else:
            return ((3/50)*(3/49) + (3/50)*(46/49)*(6/48) + (44/50)*(3/49)*(6/48))*2

    # Returns the probability of getting a double pair before the turn excluding the possibility of the board itself making a pair
    def dpair_preflop(self):
        card1 = self.__card1
        card2 = self.__card2
        val1 = card1.getValue()
        val2 = card2.getValue()
        if val1 == val2:
            return ((48 / 50) * (3 / 49) + (48 / 50) * (44 / 49) * (3 / 48))
        else:
            return ((3 / 50) * (3 / 49) + (3 / 50) * (46 / 49) * (3 / 48) + (44 / 50) * (3 / 49) * (3 / 48)) * 2

    # Returns the probability of getting a three of a kind during the flop
    def three_preflop(self):
        card1 = self.__card1
        card2 = self.__card2
        val1 = card1.getValue()
        val2 = card2.getValue()
        if val1 == val2:
            return 1
        else:
            return 1

    # Returns the odds of flopping a four of a kind
    def four_preflop(self):
        card1 = self.__card1
        card2 = self.__card2
        val1 = card1.getValue()
        val2 = card2.getValue()
        if val1 == val2:
            return 1
        else:
            return 2*((3/50)*(2/49)*(1/48))

    # Returns the odds of flopping a straight (5 cards of different suits, but in a straight sequence)
    def straight_preflop(self):
        card1 = self.__card1
        card2 = self.__card2
        val1 = card1.getValue()
        val2 = card2.getValue()
        if val1 == val2:
            return 1
        else:
            return 1

    # Returns the odds of flopping a flush (5 cards of the same suit)
    def flush_preflop(self):
        card1 = self.__card1
        card2 = self.__card2
        val1 = card1.getValue()
        val2 = card2.getValue()
        if val1 == val2:
            return 1
        else:
            return 1

    # Returns the odds of flopping a full house
    def full_preflop(self):
        card1 = self.__card1
        card2 = self.__card2
        val1 = card1.getValue()
        val2 = card2.getValue()
        if val1 == val2:
            return 1
        else:
            return 1

    # Returns the odds of flopping a straight flush
    def straightflush_preflop(self):
        card1 = self.__card1
        card2 = self.__card2
        val1 = card1.getValue()
        val2 = card2.getValue()
        if val1 == val2:
            return 1
        else:
            return 1

    # Returns the odds of flopping a royal flush
    def royalflush_preflop(self):
        card1 = self.__card1
        card2 = self.__card2
        val1 = card1.getValue()
        val2 = card2.getValue()
        if val1 == val2:
            return 1
        else:
            return 1

    ##########################################################################################
    # Flop Probabilities (Pre-turn)
    #####################################################################################à####

    def pair_flop(self):
        pass
    def dpair_flop(self):
        pass
    def three_flop(self):
        pass
    def straight_flop(self):
        pass
    def flush_flop(self):
        pass
    def full_flop(self):
        pass
    def poker_flop(self):
        pass
    def strflush_flop(self):
        pass
    def royalflush_flop(self):
        pass

    ##########################################################################################
    # Turn Probabilities (Pre-river, last hand)
    ##########################################################################################

    def pair_turn(self):
        pass
    def dpair_turn(self):
        pass
    def three_turn(self):
        pass
    def straight_turn(self):
        pass
    def flush_turn(self):
        pass
    def full_turn(self):
        pass
    def poker_turn(self):
        pass
    def strflush_turn(self):
        pass
    def royalflush_turn(self):
        pass

    ##########################################################################################
    # Total probabilities (The chances of getting a combination before the end of the hand
    ##########################################################################################

    def pair(self):
        pass
    def dpair(self):
        pass
    def three(self):
        pass
    def straight(self):
        pass
    def flush(self):
        pass
    def full(self):
        pass
    def poker(self):
        pass
    def strflush(self):
        pass
    def royalflush(self):
        pass

#####################################################################################################################################################
# Main Body
#####################################################################################################################################################

if __name__ == "__main__":

    start_time = time.time()

    # Creating a test "Texas Hold'em" deck made of 52 cards
    y = TStdDeck()

    # Creating a test hand between two players, played following the "Texas Hold'em" rules.
    hand = THand(y, 2)

    print("\nRun time:\t\t--- %s seconds ---" %(round((time.time() - start_time), 5)))