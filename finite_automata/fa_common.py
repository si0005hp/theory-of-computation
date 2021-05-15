# -*- coding: utf-8 -*-
import fa_util
from graph import Graph


class FARule:

    def __init__(self, state, character, next_state):
        self._state = state
        self._character = character
        self._next_state = next_state

    def applies_to(self, state, character):
        return self._state == state and self._character == character

    def follow(self):
        return self._next_state

    def __repr__(self):
        return '{} --{}--> {}'.format(self._state, self._character, self._next_state)


class FADesign:

    def __init__(self, start_state, accept_states, rulebook):
        self._start_state = start_state
        self._accept_states = accept_states
        self._rulebook = rulebook

    def draw(self, directory=None, filename=None):
        if directory == None:
            directory = "/tmp"
        if filename == None:
            filename = fa_util.random_str(8)

        Graph().draw(directory, filename, self._rulebook._rules, self._start_state,
                     self._accept_states)
