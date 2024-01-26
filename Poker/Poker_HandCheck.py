import Poker_TCard
import Poker_THand
import Poker_TDeck



def what_do_I_have(hand: Poker_THand.THand):
    '''

    Evaluates a given hand and evaluates the current value
    :param hand: The current table and pocket cards
    :return: A list containing the cards forming the highest combination and an fstring describing it

    '''
    lstCards = hand.getHand()
    lstValues = list(map(Poker_TCard.TCard.getValue, hand.getHand()))
    lstSuits = list(map(Poker_TCard.TCard.getSuit, hand.getHand()))

    # Returns the hierarchic index of a particular card
    def getIndex(value: str):
        index = hand.getDeck().getValues().index(value)
        return index

    # Returns a card value given the index
    def getValfromIndx(index: int):
        return hand.getDeck().getValues()[index]

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

    # Orders cards even when there are cards with the same value
    def orderCards_by_Value(lst: list) -> list:
        lstCards = []
        lstIndexes = []
        for i, card in enumerate(lst):
            index = getIndex(card.getValue())
            if index not in lstIndexes:
                lstIndexes.append(index)
            lstCards.append((index, card))
        lstIndexes.sort(reverse=True)
        lstOrdered_cards = []
        for i in lstIndexes:
            for tpl in lstCards:
                if tpl[0] == i:
                    lstOrdered_cards.append(tpl[1])
        if len(lstOrdered_cards) == len(lst):
            return lstOrdered_cards

    ######################################################################
    # Combination checks
    ######################################################################

    def checkforRoyalflush():
        royal_flush = ["T", "J", "Q", "K", "A"]
        royal = []
        j = int(0)
        if checkforStraight() and getHighest(list(map(Poker_TCard.TCard.getValue, checkforStraight()))) == 'A':
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
                return orderCards_by_Value(checkforStraight(checkforFlush()))

    def checkforFour():
        four = []
        for card in lstCards:
            value = card.getValue()
            if list(map(Poker_TCard.TCard.getValue, lstCards)).count(value) == 4:
                four.append(card)
        return orderCards_by_Value(four)

    def checkforFull():
        full = []
        highest_full = []
        three_indexes = []
        pair_indexes = []
        three_bool = int(0)
        for card in lstCards:
            value = card.getValue()
            if list(map(Poker_TCard.TCard.getValue, lstCards)).count(value) == 2:
                full.append(card)
                if getIndex(value) not in pair_indexes:
                    pair_indexes.append(getIndex(value))
            if list(map(Poker_TCard.TCard.getValue, lstCards)).count(value) == 3:
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
                return orderCards_by_Value(full)

    def checkforFlush():
        flush = []
        for suit in hand.getDeck()._suits:
            if lstSuits.count(suit) >= 5:
                for i, card in enumerate(lstCards):
                    if card.getSuit() == suit:
                        flush.append(card)
        if len(flush) > 5:
            flush = orderCards(flush)[-5:]
        return orderCards_by_Value(flush)

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

        straight = []  # The final list containing the TCards actually forming a straight
        value_straight = []  # The temp list containing the values of the TCards in a possible straight
        ace_first = [12, 0, 1, 2, 3]  # The ace can both be used before a 2 or after a K
        i_list = list(map(getIndex, orderValues(lstValues)))  # The list containing all the values of the hand

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
                        value_straight = []  # Restart from zero, all the previous
                elif len(value_straight) >= 4:  # elements don't belong to a straight
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
                # Although quite unlikely, we have to check if there are more than 5 items,
                # and pick the higher ones
                if len(flush2) > 5:
                    return flush2[-5:]
                if len(flush2) == 5:
                    return orderCards_by_Value(flush2)

        # If there's no flush we are safe reducing directly the domain of the straight
        if len(value_straight) > 5:
            value_straight = value_straight[-5:]
        for card in lst:
            index = getIndex(card.getValue())
            if index in value_straight:
                if (list(map(getIndex, hand.getValuesMap(lst)))).count(index) > 1:
                    # If there are more cards with the same value we pick only one
                    # Preference is given to the ones we hold, altough it doesn't really matter
                    for your_card in hand.getPocket():
                        if index == getIndex(your_card.getValue()):
                            straight.append(your_card)
                            break
                    straight.append(card)
                    value_straight.remove(index)
                else:
                    straight.append(card)
        if len(straight) == 5:
            return orderCards_by_Value(straight)

    def checkforThree():
        three = []
        for card in lstCards:
            value = card.getValue()
            if list(map(Poker_TCard.TCard.getValue, lstCards)).count(value) == 3:
                three.append(card)
        return orderCards_by_Value(three)

    def checkforDPair():
        dpair = []
        dvalues = []
        highest_dpair = []
        j = int(0)
        for card in lstCards:
            value = card.getValue()
            if list(map(Poker_TCard.TCard.getValue, lstCards)).count(value) == 2:
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
            return orderCards_by_Value(highest_dpair)

    def checkforPair():
        pair = []
        # Legacy version used directly the list of values, new one operates directly to the card.
        # for value in lstValues:
        #     if lstValues.count(value) == 2:
        for card in lstCards:
            if list(map(Poker_TCard.TCard.getValue, lstCards)).count(card.getValue()) == 2:
                pair.append(card)
        return orderCards_by_Value(pair)

    def checkforHigh():
        lstIndex = list(map(getIndex, lstValues))
        for card in lstCards:
            if getIndex(card.getValue()) == max(lstIndex):
                high_card = card
                return high_card

    # Check for number of cards, if below 5 -> exclude all straights and flushes, if below 4 -> exclude four of a kind
    # and double pairs, if below 3, also three of a kind
    # Check whether the flop has already come. If no, exclude all of above combinations
    pocket = hand.getNamesMap(hand.getPocket())
    table = hand.getNamesMap(hand.getTable())
    if len(lstCards) < 3:
        if checkforPair():
            return [(f'{"You have a Pair":45s}'
                     f'{"  ".join(map(str, hand.getNamesMap(checkforPair()))):30s}'
                     f'{"  ".join(map(str, pocket)):20s}{"  ".join(map(str, table)):25s}'), checkforPair()]
        else:
            return [(f'{"You have a High card":45s}'
                     f'{orderCards(hand.getPocket())[1].getName():30s}'
                     f'{"  ".join(map(str, pocket)):20s}{"  ".join(map(str, table)):25s}'),
                    orderCards(hand.getPocket())[1]]
    else:
        if checkforRoyalflush():
            return [(f'{"You have a Royal Flush":45s}'
                     f'{"  ".join(map(str, hand.getNamesMap(checkforRoyalflush()))):30s}'
                     f'{"  ".join(map(str, pocket)):20s}{"  ".join(map(str, table)):25s}'), checkforRoyalflush()]
        elif checkforStraightflush():
            return [(f'{"You have a Straight flush":45s}'
                     f'{"  ".join(map(str, hand.getNamesMap(checkforStraightflush()))):30s}'
                     f'{"  ".join(map(str, pocket)):20s}{"  ".join(map(str, table)):25s}'), checkforStraightflush()]
        elif checkforFour():
            return [(f'{"You have a Four of a kind":45s}'
                     f'{"  ".join(map(str, hand.getNamesMap(checkforFour()))):30s}'
                     f'{"  ".join(map(str, pocket)):20s}{"  ".join(map(str, table)):25s}'), checkforFour()]
        elif checkforFull():
            return [(f'{"You have a Full house":45s}'
                     f'{"  ".join(map(str, hand.getNamesMap(checkforFull()))):30s}'
                     f'{"  ".join(map(str, pocket)):20s}{"  ".join(map(str, table)):25s}'), checkforFull()]
        elif checkforFlush():
            return [(f'{"You have a Flush":45s}'
                     f'{"  ".join(map(str, hand.getNamesMap(checkforFlush()))):30s}'
                     f'{"  ".join(map(str, pocket)):20s}{"  ".join(map(str, table)):25s}'), checkforFlush()]
        elif checkforStraight():
            return [(f'{"You have a Straight":45s}'
                     f'{"  ".join(map(str, hand.getNamesMap(checkforStraight()))):30s}'
                     f'{"  ".join(map(str, pocket)):20s}{"  ".join(map(str, table)):25s}'), checkforStraight()]
        elif checkforThree():
            return [(f'{"You have a Three of a kind":45s}'
                     f'{"  ".join(map(str, hand.getNamesMap(checkforThree()))):30s}'
                     f'{"  ".join(map(str, pocket)):20s}{"  ".join(map(str, table)):25s}'), checkforThree()]
        elif checkforDPair():
            return [(f'{"You have a Double Pair":45s}'
                     f'{"  ".join(map(str, hand.getNamesMap(checkforDPair()))):30s}'
                     f'{"  ".join(map(str, pocket)):20s}{"  ".join(map(str, table)):25s}'), checkforDPair()]
        elif checkforPair():
            return [(f'{"You have a Pair":45s}'
                     f'{"  ".join(map(str, hand.getNamesMap(checkforPair()))):30s}'
                     f'{"  ".join(map(str, pocket)):20s}'
                     f'{"  ".join(map(str, table)):25s}'), checkforPair()]
        else:
            return [(f'{"You have a High card":45s}'
                     f'{orderCards(hand.getPocket())[1].getName():30s}'
                     f'{"  ".join(map(str, pocket)):20s}{"  ".join(map(str, table)):25s}'),
                    orderCards(hand.getPocket())[1]]
