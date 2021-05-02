from pda_common import PDARule, PDAConfiguration, Stack


class DPDARulebook:

    def __init__(self, rules):
        self._rules = rules

    def next_configuration(self, configuration, character):
        return self.rule_for(configuration, character).follow(configuration)

    def rule_for(self, configuration, character):
        matched_rules = [r for r in self._rules if r.applies_to(configuration, character)]
        return None if len(matched_rules) == 0 else next(iter(matched_rules))

    def applies_to(self, configuration, character):
        return self.rule_for(configuration, character) != None

    def follow_free_moves(self, configuration):
        if self.applies_to(configuration, None):
            return self.follow_free_moves(self.next_configuration(configuration, None))
        else:
            return configuration


class DPDA:

    def __init__(self, current_configuration, accept_states, rulebook):
        self._current_configuration = current_configuration
        self._accept_states = accept_states
        self._rulebook = rulebook

    def accepting(self):
        return self.current_configuration().state in self._accept_states

    def read_character(self, character):
        self._current_configuration = self.next_configuration(character)

    def read_string(self, string):
        for c in string:
            if not self.is_stuck():
                self.read_character(c)

    def current_configuration(self):
        return self._rulebook.follow_free_moves(self._current_configuration)

    def next_configuration(self, character):
        if self._rulebook.applies_to(self.current_configuration(), character):
            return self._rulebook.next_configuration(self.current_configuration(), character)
        else:
            return self.current_configuration().stuck()

    def is_stuck(self):
        return self.current_configuration().is_stuck()


class DPDADesign:

    def __init__(self, start_state, bottom_character, accept_states, rulebook):
        self._start_state = start_state
        self._bottom_character = bottom_character
        self._accept_states = accept_states
        self._rulebook = rulebook

    def accepts(self, string):
        dpda = self.to_dpda()
        dpda.read_string(string)
        return dpda.accepting()

    def to_dpda(self):
        start_stack = Stack([self._bottom_character])
        start_configuration = PDAConfiguration(self._start_state, start_stack)
        return DPDA(start_configuration, self._accept_states, self._rulebook)
