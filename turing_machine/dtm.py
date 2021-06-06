# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
sys.path.append('../finite_automata')

import finite_automata.fa_util as fa_util
from finite_automata.graph import Graph


class Tape:

    def __init__(self, left, middle, right, blank):
        self.left = left
        self.middle = middle
        self.right = right
        self.blank = blank

    def __str__(self):
        return "{}({}){}".format(''.join(self.left), self.middle, ''.join(self.right))

    def __repr__(self):
        return "<Tape {}>".format(self.__str__())

    def write(self, character):
        return Tape(self.left, character, self.right, self.blank)

    def move_head_left(self):
        return Tape(
            self.left[:-1],
            self.left[-1] if len(self.left) > 0 else self.blank,
            [self.middle, *self.right],
            self.blank,
        )

    def move_head_right(self):
        return Tape(
            [*self.left, self.middle],
            self.right[0] if len(self.right) > 0 else self.blank,
            self.right[1:],
            self.blank,
        )


class TMConfiguration:

    def __init__(self, state, tape):
        self.state = state
        self.tape = tape

    def __repr__(self):
        return '<state: {}, tape: {}>'.format(self.state, self.tape)


class TMRule:

    def __init__(self, state, character, next_state, write_character, direction):
        self.state = state
        self.character = character
        self.next_state = next_state
        self.write_character = character if write_character == None else write_character
        self.direction = direction

    def applies_to(self, configuration):
        return self.state == configuration.state and self.character == configuration.tape.middle

    def follow(self, configuration):
        return TMConfiguration(self.next_state, self.next_tape(configuration))

    def next_tape(self, configuration):
        written_tape = configuration.tape.write(self.write_character)

        if self.direction == 'L':
            return written_tape.move_head_left()
        elif self.direction == 'R':
            return written_tape.move_head_right()


class DTMRulebook:

    def __init__(self, rules):
        self.rules = rules

    def rule_for(self, configuration):
        matched_rules = [r for r in self.rules if r.applies_to(configuration)]
        return None if len(matched_rules) == 0 else next(iter(matched_rules))

    def applies_to(self, configuration):
        return self.rule_for(configuration) != None

    def next_configuration(self, configuration):
        return self.rule_for(configuration).follow(configuration)


class DTMGraph(Graph):

    # Override
    def make_label(self, rule):
        return '{}/{};{}'.format(rule.character, rule.write_character, rule.direction)

    # Override
    def format_labels(self, labels):
        return '\n'.join(labels)

    # Override
    def get_state(self, rule):
        return rule.state

    # Override
    def get_next_state(self, rule):
        return rule.next_state


class DTM:

    def __init__(self, current_configuration, accept_states, rulebook, is_debug=False):
        self.current_configuration = current_configuration
        self.accept_states = accept_states
        self.rulebook = rulebook
        self.is_debug = is_debug
        self.step_counter = 0

    def accepting(self):
        return self.current_configuration.state in self.accept_states

    def step(self):
        self.current_configuration = self.rulebook.next_configuration(self.current_configuration)
        self.step_counter += 1

        self.debug_state()

    def run(self):
        self.debug_state()

        while not self.accepting() and not self.is_stuck():
            self.step()

    def is_stuck(self):
        return not self.accepting() and not self.rulebook.applies_to(self.current_configuration)

    def debug_state(self):
        if self.is_debug:
            print('Step: {}\t{}'.format(self.step_counter, self.current_configuration))


class DTMDesign:

    def __init__(self, start_state, accept_states, rulebook):
        self.start_state = start_state
        self.accept_states = accept_states
        self.rulebook = rulebook

    def new_dtm(self, tape, is_debug):
        return DTM(
            TMConfiguration(self.start_state, tape), self.accept_states, self.rulebook, is_debug)

    def accepts(self, tape, is_debug=False):
        dtm = self.new_dtm(tape, is_debug)
        dtm.run()
        return dtm.accepting()

    def draw(self, directory=None, filename=None):
        if directory == None:
            directory = "/tmp"
        if filename == None:
            filename = fa_util.random_str(8)

        DTMGraph().draw(directory, filename, self.rulebook.rules, self.start_state,
                        self.accept_states)
