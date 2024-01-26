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
        return (f"Please insert a valid card!\n"
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
        return f"Card already exist!\nYou cannot have duplicates of the same card in a standard deck! "
