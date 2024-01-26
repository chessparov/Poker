import Poker_Exceptions

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
                raise Poker_Exceptions.ExceptInvalidCardLenght
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
