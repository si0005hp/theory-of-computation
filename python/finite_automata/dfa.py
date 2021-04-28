from fa_common import FARule, FADesign


class DFARulebook:

    def __init__(self, rules):
        self._rules = rules

    def next_state(self, state, character):
        return self.rule_for(state, character).follow()

    def rule_for(self, state, character):
        return next(r for r in self._rules if r.applies_to(state, character))


class DFA:

    def __init__(self, current_state, accept_states, rulebook):
        self._current_state = current_state
        self._accept_states = accept_states
        self._rulebook = rulebook

    def accepting(self):
        return self._current_state in self._accept_states

    def read_character(self, character):
        self._current_state = self._rulebook.next_state(self._current_state, character)

    def read_string(self, string):
        for c in string:
            self.read_character(c)


class DFADesign(FADesign):

    def accepts(self, string):
        dfa = DFA(self._start_state, self._accept_states, self._rulebook)
        dfa.read_string(string)
        return dfa.accepting()
