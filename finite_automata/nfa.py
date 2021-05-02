from fa_common import FARule, FADesign


class NFARulebook:

    def __init__(self, rules):
        self._rules = rules

    def next_states(self, states, character):
        return frozenset(sum([self.follow_rules_for(s, character) for s in states], []))

    def follow_rules_for(self, state, character):
        return [r.follow() for r in self.rules_for(state, character)]

    def rules_for(self, state, character):
        return [r for r in self._rules if r.applies_to(state, character)]

    def follow_free_moves(self, states):
        more_states = self.next_states(states, None)
        if more_states.issubset(states):
            return frozenset(states)
        else:
            return self.follow_free_moves(states | more_states)

    def alphabet(self):
        return frozenset(r._character for r in self._rules if r._character != None)


class NFA:

    def __init__(self, current_states, accept_states, rulebook):
        self._current_states = current_states
        self._accept_states = accept_states
        self._rulebook = rulebook

    def accepting(self):
        return len(self.current_states() & self._accept_states) > 0

    def read_character(self, character):
        self._current_states = self._rulebook.next_states(self.current_states(), character)

    def read_string(self, string):
        for c in string:
            self.read_character(c)

    def current_states(self):
        return self._rulebook.follow_free_moves(self._current_states)


class NFADesign(FADesign):

    def accepts(self, string):
        nfa = self.to_nfa()
        nfa.read_string(string)
        return nfa.accepting()

    def to_nfa(self, current_states=None):
        if current_states == None:
            current_states = frozenset({self._start_state})
        return NFA(current_states, self._accept_states, self._rulebook)
