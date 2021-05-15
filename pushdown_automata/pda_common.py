# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
sys.path.append('../finite_automata')

import graphviz
from functools import reduce
import finite_automata.fa_util as fa_util
from finite_automata.graph import Graph


class Stack:

    def __init__(self, contents=None):
        self._contents = [] if contents == None else contents

    def push(self, character):
        return Stack(self._contents + [character])

    def pop(self):
        return Stack(self._contents[:-1])

    def top(self):
        return self._contents[-1]

    def __str__(self):
        return ''.join(self._contents)

    def __repr__(self):
        return self.__str__()


class PDAConfiguration:
    STUCK_STATE = object()

    def __init__(self, state, stack):
        self.state = state
        self.stack = stack

    def stuck(self):
        return PDAConfiguration(self.STUCK_STATE, self.stack)

    def is_stuck(self):
        return self.state == self.STUCK_STATE

    def __hash__(self):
        return hash(self.__str__())

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __str__(self):
        return '<state: {}, stack: {}>'.format('stucked' if self.is_stuck() else self.state,
                                               self.stack)

    def __repr__(self):
        return self.__str__()


class PDARule:

    def __init__(self, state, character, next_state, pop_character, push_characters):
        self._state = state
        self._character = character
        self._next_state = next_state
        self._pop_character = pop_character
        self._push_characters = push_characters

    def applies_to(self, configuration, character):
        return self._state == configuration.state and self._pop_character == configuration.stack.top(
        ) and self._character == character

    def follow(self, configuration):
        return PDAConfiguration(self._next_state, self.next_stack(configuration))

    def next_stack(self, configuration):
        popped_stack = configuration.stack.pop()
        return reduce(lambda stack, c: stack.push(c), reversed(self._push_characters), popped_stack)


class PDAGraph(Graph):

    # Override
    def make_label(self, rule):
        char = "ε" if rule._character == None else rule._character
        pop_char = rule._pop_character
        push_chars = ''.join(rule._push_characters)
        return '{};{}/{}'.format(char, pop_char, push_chars)

    # Override
    def format_labels(self, labels):
        return ',\n'.join(labels)


class PDADesign:

    def __init__(self, start_state, bottom_character, accept_states, rulebook):
        self._start_state = start_state
        self._bottom_character = bottom_character
        self._accept_states = accept_states
        self._rulebook = rulebook

    def draw(self, directory=None, filename=None):
        if directory == None:
            directory = "/tmp"
        if filename == None:
            filename = fa_util.random_str(8)

        PDAGraph().draw(directory, filename, self._rulebook._rules, self._start_state,
                        self._accept_states)
