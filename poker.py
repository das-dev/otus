#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------
# Реализуйте функцию best_hand, которая принимает на вход
# покерную "руку" (hand) из 7ми карт и возвращает лучшую
# (относительно значения, возвращаемого hand_rank)
# "руку" из 5ти карт. У каждой карты есть масть(suit) и
# ранг(rank)
# Масти: трефы(clubs, C), пики(spades, S), червы(hearts, H), бубны(diamonds, D)
# Ранги: 2, 3, 4, 5, 6, 7, 8, 9, 10 (ten, T), валет (jack, J), дама (queen, Q), король (king, K), туз (ace, A)
# Например: AS - туз пик (ace of spades), TH - дестяка черв (ten of hearts), 3C - тройка треф (three of clubs)

# Задание со *
# Реализуйте функцию best_wild_hand, которая принимает на вход
# покерную "руку" (hand) из 7ми карт и возвращает лучшую
# (относительно значения, возвращаемого hand_rank)
# "руку" из 5ти карт. Кроме прочего в данном варианте "рука"
# может включать джокера. Джокеры могут заменить карту любой
# масти и ранга того же цвета, в колоде два джокерва.
# Черный джокер '?B' может быть использован в качестве треф
# или пик любого ранга, красный джокер '?R' - в качестве черв и бубен
# любого ранга.

# Одна функция уже реализована, сигнатуры и описания других даны.
# Вам наверняка пригодится itertools.
# Можно свободно определять свои функции и т.п.
# -----------------
import itertools
from collections import Counter


RANKS = dict(zip('23456789TJQKA', range(2, 15)))
RED_CARDS = [''.join([rank, suite]) for rank in RANKS for suite in 'HD']
BLACK_CARDS = [''.join([rank, suite]) for rank in RANKS for suite in 'SC']
RED_JOKER = '?R'
BLACK_JOKER = '?B'
RANK_SIDE = 0
SUIT_SIDE = 1
HAND_SIZE = 5



def hand_rank(hand):
    """Возвращает значение определяющее ранг 'руки'"""
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):
        return (8, max(ranks))
    elif kind(4, ranks):
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):
        return (5, ranks)
    elif straight(ranks):
        return (4, max(ranks))
    elif kind(3, ranks):
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):
        return (1, kind(2, ranks), ranks)
    else:
        return (0, ranks)


def card_ranks(hand):
    """Возвращает список рангов (его числовой эквивалент),
    отсортированный от большего к меньшему"""

    return sorted(RANKS[card[RANK_SIDE]] for card in hand)


def flush(hand):
    """Возвращает True, если все карты одной масти"""

    return len(set(card[SUIT_SIDE] for card in hand)) == 1


def straight(ranks):
    """Возвращает True, если отсортированные ранги формируют последовательность 5ти,
    где у 5ти карт ранги идут по порядку (стрит)"""

    return ranks == range(ranks[0], ranks[-1])


def kind(n, ranks):
    """Возвращает первый ранг, который n раз встречается в данной руке.
    Возвращает None, если ничего не найдено"""

    counts = Counter(ranks)
    for rank in ranks:
        if counts[rank] == n:
            return rank


def two_pair(ranks):
    """Если есть две пары, то возврщает два соответствующих ранга,
    иначе возвращает None"""

    uniq_ranks = set(ranks)
    if len(uniq_ranks) == HAND_SIZE - 2:
        not_pair = kind(1, ranks)
        return [rank for rank in uniq_ranks if rank != not_pair]


def best_hand(hand):
    """Из "руки" в 7 карт возвращает лучшую "руку" в 5 карт """

    best = None
    for version in itertools.permutations(hand, HAND_SIZE):
        if not best or hand_rank(version) > hand_rank(best):
            best = version
    return best


def best_wild_hand(hand):
    """best_hand но с джокерами"""

    jokers = RED_JOKER, BLACK_JOKER
    jokers_on_hand = [card for card in hand if card in jokers]
    hands = []
    red_cards = RED_CARDS if RED_JOKER in jokers_on_hand else [None]
    black_cards = BLACK_CARDS if BLACK_JOKER in jokers_on_hand else [None]
    cards = [card for card in hand if card not in jokers]
    for red_card in red_cards:
        for black_card in black_cards:
            extra_hand = filter(bool, [red_card, black_card]) + cards
            hands.append(extra_hand)

    best = None
    for hand in hands:
        for version in itertools.permutations(hand, HAND_SIZE):
            print version, hand_rank(version)
            if not best or hand_rank(version) > hand_rank(best):
                best = version
    return best


def test_best_hand():
    print "test_best_hand..."
    assert (sorted(best_hand("6C 7C 8C 9C TC 5C JS".split()))
            == ['6C', '7C', '8C', '9C', 'TC'])
    assert (sorted(best_hand("TD TC TH 7C 7D 8C 8S".split()))
            == ['8C', '8S', 'TC', 'TD', 'TH'])
    assert (sorted(best_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    print 'OK'


def test_best_wild_hand():
    print "test_best_wild_hand..."
    print (sorted(best_wild_hand("6C 7C 8C 9C TC 5C ?B".split())))
    assert (sorted(best_wild_hand("6C 7C 8C 9C TC 5C ?B".split()))
            == ['7C', '8C', '9C', 'JC', 'TC'])
    assert (sorted(best_wild_hand("TD TC 5H 5C 7C ?R ?B".split()))
            == ['7C', 'TC', 'TD', 'TH', 'TS'])
    assert (sorted(best_wild_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    print 'OK'


if __name__ == '__main__':
    test_best_hand()
    test_best_wild_hand()
