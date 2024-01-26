import Poker_TCard
import Poker_THand

def pair_preflop(pocket):
    val1 = pocket[0].getValue()
    val2 = pocket[1].getValue()
    if val1 == val2:
        return 1
    else:
        return (6 / 50) + (44 / 50) * (6 / 49) + (44 / 50) * (43 / 49) * (6 / 48)


# Returns the probability of getting a double pair before the turn
def dpair_preflop_table(pocket):
    val1 = pocket[0].getValue()
    val2 = pocket[1].getValue()
    if val1 == val2:
        return (48 / 50) * (3 / 49) + (48 / 50) * (44 / 49) * (3 / 48)
    else:
        return ((3 / 50) * (3 / 49) + (3 / 50) * (46 / 49) * (6 / 48) + (44 / 50) * (3 / 49) * (6 / 48)) * 2


# Returns the probability of getting a double pair before the turn excluding the possibility of the board it making a pair
def dpair_preflop(pocket):
    val1 = pocket[0].getValue()
    val2 = pocket[1].getValue()
    if val1 == val2:
        return ((48 / 50) * (3 / 49) + (48 / 50) * (44 / 49) * (3 / 48))
    else:
        return ((3 / 50) * (3 / 49) + (3 / 50) * (46 / 49) * (3 / 48) + (44 / 50) * (3 / 49) * (3 / 48)) * 2


# Returns the probability of getting a three of a kind during the flop
def three_preflop(pocket):
    val1 = pocket[0].getValue()
    val2 = pocket[1].getValue()
    if val1 == val2:
        return 1
    else:
        return 1


# Returns the odds of flopping a four of a kind
def four_preflop(pocket):
    val1 = pocket[0].getValue()
    val2 = pocket[1].getValue()
    if val1 == val2:
        return 1
    else:
        return 2 * ((3 / 50) * (2 / 49) * (1 / 48))


# Returns the odds of flopping a straight (5 cards of different suits, but in a straight sequence)
def straight_preflop(pocket):
    val1 = pocket[0].getValue()
    val2 = pocket[1].getValue()
    if val1 == val2:
        return 1
    else:
        return 1


# Returns the odds of flopping a flush (5 cards of the same suit)
def flush_preflop(pocket):
    val1 = pocket[0].getValue()
    val2 = pocket[1].getValue()
    if val1 == val2:
        return 1
    else:
        return 1


# Returns the odds of flopping a full house
def full_preflop(pocket):
    val1 = pocket[0].getValue()
    val2 = pocket[1].getValue()
    if val1 == val2:
        return 1
    else:
        return 1


# Returns the odds of flopping a straight flush
def straightflush_preflop(pocket):
    val1 = pocket[0].getValue()
    val2 = pocket[1].getValue()
    if val1 == val2:
        return 1
    else:
        return 1


# Returns the odds of flopping a royal flush
def royalflush_preflop(pocket):
    val1 = pocket[0].getValue()
    val2 = pocket[1].getValue()
    if val1 == val2:
        return 1
    else:
        return 1