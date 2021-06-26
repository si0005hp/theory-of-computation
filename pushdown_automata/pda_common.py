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
        return self._contents[-1] if len(self._contents) > 0 else None

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

    class LabelMaker:

        def char(self, rule):
            return "ε" if rule._character == None else rule._character

        def make_label(self, rule):
            pass

    class RigidLabelMaker(LabelMaker):

        def make_label(self, rule):
            pop_char = rule._pop_character
            push_chars = ''.join(rule._push_characters)
            return '{};{}/{}'.format(self.char(rule), pop_char, push_chars)

    class SimpleLabelMaker(LabelMaker):

        def make_label(self, rule):
            pop_char = rule._pop_character
            push_char = None
            if len(rule._push_characters) == 0:
                push_char = 'ε'
            elif len(rule._push_characters) == 1:
                push_char = rule._push_characters[0]
            elif len(rule._push_characters) == 2:
                pop_char = 'ε'
                push_char = rule._push_characters[0]
            else:
                raise RuntimeError('Illegal push_characters size. It must be between 0 and 2.')

            return '{},{}→{}'.format(self.char(rule), pop_char, push_char)

    def __init__(self, bottom_character, use_label_simple=False):
        self.bottom_character = bottom_character
        self.label_maker = self.SimpleLabelMaker() if use_label_simple else self.RigidLabelMaker()

    # Override
    def make_label(self, rule):
        return self.label_maker.make_label(rule)

    # Override
    def format_labels(self, labels):
        # NOTE: Currently only PDA eliminates dupulication.
        return '\n'.join(set(labels))

    # Override
    def add_start_edge(self, graph, start_state):
        # For PDA, insert additional state for pushing stack bottom character
        additional_start_state = 'S'
        graph.node(additional_start_state, **{'root': 'true', 'shape': 'circle'})
        graph.edge(
            additional_start_state, self.state_to_str(start_state),
            self.make_label(
                PDARule(additional_start_state, None, self.state_to_str(start_state),
                        self.bottom_character, [self.bottom_character, self.bottom_character])))

        # Then add arrow to additional_start_state
        dummy_node = fa_util.random_str(8)
        graph.node(dummy_node, style="invis", shape="point")
        graph.edge(dummy_node, additional_start_state, style="bold")


class PDADesign:

    def __init__(self, start_state, bottom_character, accept_states, rulebook):
        self._start_state = start_state
        self._bottom_character = bottom_character
        self._accept_states = accept_states
        self._rulebook = rulebook

    def draw(self, directory=None, filename=None, use_label_simple=False):
        if directory == None:
            directory = "/tmp"
        if filename == None:
            filename = fa_util.random_str(8)

        PDAGraph(self._bottom_character,
                 use_label_simple).draw(directory, filename, self._rulebook._rules,
                                        self._start_state, self._accept_states)
