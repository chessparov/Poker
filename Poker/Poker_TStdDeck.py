import numpy as np
import Poker_TCard
import Poker_TDeck

class TStdDeck(Poker_TDeck.TDeck):
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
                new_card = Poker_TCard.TCard(new_card_name)
                card_matrix.append(new_card)
                card_names_matrix.append(new_card_name)
        card_matrix = np.reshape(card_matrix, (4, 13))
        card_names_matrix = np.reshape(card_names_matrix, (4, 13))
        self._cardnames = np.array(card_names_matrix, dtype=str)
        self._cards = np.array(card_matrix, dtype=Poker_TCard.TCard)
        self._cardsnumber = 52
