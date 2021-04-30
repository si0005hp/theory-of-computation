from pda_common import PDARule, PDAConfiguration, Stack


class NPDARulebook:

    def __init__(self, rules):
        self._rules = rules

    def next_configurations(self, configurations, character):
        return frozenset(sum([self.follow_rules_for(c, character) for c in configurations], []))

    def follow_rules_for(self, configuration, character):
        return [r.follow(configuration) for r in self.rules_for(configuration, character)]

    def rules_for(self, configuration, character):
        return [r for r in self._rules if r.applies_to(configuration, character)]

    def follow_free_moves(self, configurations):
        more_configurations = self.next_configurations(configurations, None)

        if more_configurations.issubset(configurations):
            return frozenset(configurations)
        else:
            return self.follow_free_moves(configurations | more_configurations)


class NPDA:

    def __init__(self, current_configurations, accept_states, rulebook):
        self._current_configurations = current_configurations
        self._accept_states = accept_states
        self._rulebook = rulebook

    def accepting(self):
        return len([c for c in self.current_configurations() if c.state in self._accept_states]) > 0

    def read_character(self, character):
        self._current_configurations = self._rulebook.next_configurations(
            self.current_configurations(), character)

    def read_string(self, string):
        for c in string:
            self.read_character(c)

    def current_configurations(self):
        return self._rulebook.follow_free_moves(self._current_configurations)


class NPDADesign:

    def __init__(self, start_state, bottom_character, accept_states, rulebook):
        self._start_state = start_state
        self._bottom_character = bottom_character
        self._accept_states = accept_states
        self._rulebook = rulebook

    def accepts(self, string):
        npda = self.to_npda()
        npda.read_string(string)
        return npda.accepting()

    def to_npda(self):
        start_stack = Stack([self._bottom_character])
        start_configuration = PDAConfiguration(self._start_state, start_stack)
        return NPDA(frozenset({start_configuration}), self._accept_states, self._rulebook)
