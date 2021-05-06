# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
sys.path.append('../finite_automata')

from functools import reduce
from finite_automata.fa_util import random_str
from finite_automata.nfa import NFARulebook, NFADesign, FARule


class TmpState:

    def __init__(self):
        self.hash = random_str(6)

    def __str__(self):
        return self.hash


class Pattern:

    def to_nfa_design(self):
        pass

    def precedence(self):
        pass

    def __str__(self):
        pass

    def __repr__(self):
        return self.__str__()

    def bracket(self, outer_precedence):
        if self.precedence() < outer_precedence:
            return '({})'.format(str(self))
        else:
            return str(self)

    def matches(self, string):
        return self.to_nfa_design().accepts(string)


class Literal(Pattern):

    def __init__(self, character):
        self.character = character

    def precedence(self):
        return 3

    def __str__(self):
        return self.character

    def to_nfa_design(self):
        start_state = TmpState()
        accept_state = TmpState()

        return NFADesign(start_state, {accept_state},
                         NFARulebook([
                             FARule(start_state, self.character, accept_state),
                         ]))


class Empty(Pattern):

    def precedence(self):
        return 3

    def __str__(self):
        return 'ε'

    def to_nfa_design(self):
        start_state = TmpState()

        return NFADesign(start_state, {start_state}, NFARulebook([]))


class Choose(Pattern):

    def __init__(self, first, second):
        self.first = first
        self.second = second

    def precedence(self):
        return 0

    def __str__(self):
        return '|'.join(pattern.bracket(self.precedence()) for pattern in [self.first, self.second])

    def to_nfa_design(self):
        first_nfa_design = self.first.to_nfa_design()
        second_nfa_design = self.second.to_nfa_design()

        start_state = TmpState()
        accept_states = first_nfa_design._accept_states | second_nfa_design._accept_states
        rules = first_nfa_design._rulebook._rules + second_nfa_design._rulebook._rules
        extra_rules = [
            FARule(start_state, None, nfa._start_state)
            for nfa in [first_nfa_design, second_nfa_design]
        ]

        return NFADesign(start_state, accept_states, NFARulebook(rules + extra_rules))


class Concatenate(Pattern):

    def __init__(self, first, second):
        self.first = first
        self.second = second

    def precedence(self):
        return 1

    def __str__(self):
        return ''.join(pattern.bracket(self.precedence()) for pattern in [self.first, self.second])

    def to_nfa_design(self):
        first_nfa_design = self.first.to_nfa_design()
        second_nfa_design = self.second.to_nfa_design()

        start_state = first_nfa_design._start_state
        accept_states = second_nfa_design._accept_states
        rules = first_nfa_design._rulebook._rules + second_nfa_design._rulebook._rules
        extra_rules = [
            FARule(s, None, second_nfa_design._start_state) for s in first_nfa_design._accept_states
        ]

        return NFADesign(start_state, accept_states, NFARulebook(rules + extra_rules))


class Repeat(Pattern):

    def __init__(self, pattern):
        self.pattern = pattern

    def precedence(self):
        return 2

    def __str__(self):
        return self.pattern.bracket(self.precedence()) + '*'

    def to_nfa_design(self):
        pattern_nfa_design = self.pattern.to_nfa_design()

        start_state = TmpState()
        accept_states = pattern_nfa_design._accept_states | {start_state}
        rules = pattern_nfa_design._rulebook._rules
        extra_rules = [
            FARule(s, None, pattern_nfa_design._start_state)
            for s in pattern_nfa_design._accept_states
        ] + [FARule(start_state, None, pattern_nfa_design._start_state)]

        return NFADesign(start_state, accept_states, NFARulebook(rules + extra_rules))


### utils
def concat_from_str(string):
    literals = [Literal(c) for c in string]
    return reduce(lambda l1, l2: Concatenate(l1, l2), literals)


def choose_from_chars(c1, c2):
    return Choose(Literal(c1), Literal(c2))


def concats(patterns):
    return reduce(lambda p1, p2: Concatenate(p1, p2), patterns)


def chooses(patterns):
    return reduce(lambda p1, p2: Choose(p1, p2), patterns)
