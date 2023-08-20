import random
import numpy as np
import itertools
import more_itertools


class Card:
    def __init__(self, rank, suit) -> None:
        self.rank = rank
        self.suit = suit

    def __repr__(self) -> str:
        suit_str = self.rank
        if self.rank == 14:
            suit_str = 'A'
        elif self.rank == 13:
            suit_str = 'K'
        elif self.rank == 12:
            suit_str = 'Q'
        elif self.rank == 11:
            suit_str = 'J'
        if self.suit == 0:
            rank_str = '♠'
        elif self.suit == 1:
            rank_str = '♣'
        elif self.suit == 2:
            rank_str = '♦'
        else:
            rank_str = '♥'
        return f'{suit_str}{rank_str}'

    def __eq__(self, __value: object) -> bool:

        if isinstance(__value, Card):
            return self.rank == __value.rank and self.suit == __value.suit
        return False

    def tuple(self) -> tuple:
        return (self.rank, self.suit)

    def __str__(self) -> str:
        return self.__repr__()


def group_by_rank(cards):
    cards2 = [[] for _ in range(13)]
    for c in cards:
        cards2[c.rank-2].append(c)
    return cards2


def group_by_suit(cards):
    cards1 = [[] for _ in range(4)]
    for c in cards:
        cards1[c.suit].append(c)

    return cards1


def pick_best_hand(cards=None):
    """
    """
    if cards is None:
        cards = ((2, 1), (3, 1), (3, 2), (3, 3), (4, 0), (5, 1), (5, 2),
                 (6, 1), (6, 2), (6, 3), (7, 1), (7, 2), (7, 3), (14, 3))

        # cards = ((2, 1), (3, 1), (3, 2), (3, 3), (4, 1), (5, 1), (5, 2))
        cards = [Card(i, j) for i, j in cards]

    cardsS = group_by_suit(cards)
    cardsR = group_by_rank(cards)[::-1]
    a = [len(i) for i in cardsR]
    b = [len(i) for i in cardsS]
    a1 = [i >= 1 for i in a]
    a2 = tuple(more_itertools.sliding_window(a1, 5))

    # straigh flush
    for i, j in enumerate(a2):
        if (True,)*5 == j:
            start_index = i
            straigh_cards = [cardsR[i]
                             for i in range(start_index, start_index+5)]
            ()
            target_suit = next(k for k in straigh_cards if len(k) == 1)[0].suit
            straigh_flush_cards = [
                k2 for k in straigh_cards for k2 in k if k2.suit == target_suit]
            if len(straigh_flush_cards) == 5:
                if(straigh_flush_cards)[0].rank == 14:
                    # royal flush
                    return 1, 'royal flush', straigh_flush_cards, []
                else:
                    return 2, 'straigh flush', straigh_flush_cards, []

    # four of kind
    if 4 in a:
        return 3, 'four of kind', cardsR[a.index(4)], []

    c3 = list.count(a, 3)
    c2 = list.count(a, 2)

    # full house
    if c3 >= 2 or (c3 == 1 and c2 >= 1):

        index1 = a.index(3)

        # initial at lowest
        index21 = 13
        index22 = 13

        if c3 >= 2:
            # index of three of kind
            index21 = a.index(3, index1+1)

        if c2 >= 1:

            # index of pair
            index22 = a.index(2)

        # choose best index out of two
        return 4, 'full house', cardsR[index1], cardsR[min(index21, index22)][:2]

    # flush
    for i in cardsS:
        if len(i) >= 5:
            return 5, 'flush', i[-5:], []

    # straight
    if (True,)*5 in a2:
        start_index = a2.index((True,)*5)
        return 6, 'straight', [cardsR[i][0] for i in range(start_index, start_index+5)], []

    # three of kind
    if c3 == 1 and c2 == 0:
        return 7, 'three of kind', cardsR[a.index(3)], []

    # two pair
    if c2 >= 2:
        index1 = a.index(2)
        return 8, 'two pair', cardsR[index1], cardsR[a.index(2, index1+1)]

    # pair
    if c2 >= 1:
        index1 = a.index(2)
        return 9, 'pair', cardsR[index1], []

    # high card
    return 10, 'high card', [j for i in cardsR for j in i][:5], []


def pick_best_hand_ext(cards=None):
    i, n, j, k = pick_best_hand(cards)
    return (n, j, k, i, 14-j[0].rank, 14-k[0].rank if k else 0)


def new_decks(shuffle=True, fromCards=None, excludeCards=None):
    if fromCards is None:
        decks = [Card(i, j) for i, j in itertools.product(
            list(range(2, 15)), list(range(0, 4)))]
    else:
        decks = fromCards
    if excludeCards is not None:
        for c in excludeCards:
            if c in decks:
                decks.remove(c)
    if shuffle:
        random.shuffle(decks)
    return decks


# new_decks(excludeCards=[Card(2, 0)], shuffle=False)


def calc_result(hands, sharedCards):
    """
    find winner
    example return 
    [(2, 'pair', [A♥, A♠], [], 9, 0, 0),
    (0, 'pair', [8♥, 8♣], [], 9, 6, 0),
    (1, 'high card', [A♠, 10♦, 9♣, 8♣, 6♣], [], 10, 0, 0),
    (3, 'high card', [A♠, K♠, J♥, 8♣, 6♣], [], 10, 0, 0),
    (4, 'high card', [A♠, 8♣, 7♠, 6♣, 5♥], [], 10, 0, 0)]
    """
    return sorted([(j,)+pick_best_hand_ext(i+sharedCards)
                   for j, i in enumerate(hands)], key=lambda x: x[4:7])


def draw(preHands=None, preSharedCards=None, ntable=5):
    """
    draw new or continue exists game
    ntable: draw to number of card in table 
    """
    if preHands is None and preSharedCards is None:
        decks = new_decks(True)
        preHands = [decks[i*2:i*2+2] for i in range(5)]
        sharedCards = decks[-ntable:] if ntable > 0 else []
        return preHands, sharedCards
    elif preHands is not None:
        if preSharedCards is None:
            preSharedCards = []
        decks = new_decks(shuffle=True, excludeCards=[
                          *(j for i in preHands for j in i), *preSharedCards])
        nrm = ntable-len(preSharedCards)
        sharedCards = preSharedCards + decks[-nrm:] if ntable > 0 else []
        return preHands, sharedCards


def calcWinPC(hands, sharedCards, nSimulation=1000):
    """calc winning percent by nSimulation
    larger nSimulation more accurate
    """
    a = []
    for _ in range(nSimulation):
        tempHands, tempSharedCards = draw(
            preHands=hands, preSharedCards=sharedCards)
        result = calc_result(tempHands, tempSharedCards)
        winnerId = result[0][0]
        a.append(winnerId)
    b = np.array(np.unique(a, return_counts=True))
    b = [b[1, :][b[0, :] == i] for i in range(5)]
    b = [i[0]/nSimulation if len(i) > 0 else 0 for i in b]
    return b


if __name__ == '__main__':
    """
    winning percent:
    0 [4♠, A♥] : 9.70 %
    1 [4♣, 7♣] : 44.34 %
    2 [4♥, A♠] : 3.50 %
    3 [10♦, J♥] : 39.74 %
    4 [5♣, 2♠] : 2.72 %

    drew table: [8♠, 3♦, 7♠]

    example game:

    draw table: [8♠, 3♦, 7♠, 2♣, 8♦] 

    (1, 'two pair', [8♠, 8♦], [7♣, 7♠], 8, 6, 7)
    (4, 'two pair', [8♠, 8♦], [2♠, 2♣], 8, 6, 12)
    (0, 'pair', [8♠, 8♦], [], 9, 6, 0)
    (2, 'pair', [8♠, 8♦], [], 9, 6, 0)
    (3, 'pair', [8♠, 8♦], [], 9, 6, 0)
    """
    preHands, preTable = draw(ntable=3)

    b = calcWinPC(preHands, preTable, nSimulation=1000)

    # print("winning percent:\n")
    for k, i, j in zip(range(5), preHands, b):
        print(k, i, ':', '{:.2f}'.format(j*100), '%')
    print('\nshared cards:', preTable)

    print("\nexample game:\n")

    hands, table = draw(preHands=preHands, preSharedCards=preTable)
    result = calc_result(hands, table)
    # print(*hands, sep='\n')
    print('shared cards:', table, '\n', sep=' ')
    print(*result, sep='\n')
