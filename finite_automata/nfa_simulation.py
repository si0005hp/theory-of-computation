from nfa import NFARulebook, FARule, NFADesign
from dfa import DFARulebook, DFADesign


class NFASimulation:

    def __init__(self, nfa_design):
        self._nfa_design = nfa_design

    def next_state(self, state, character):
        nfa = self._nfa_design.to_nfa(state)
        nfa.read_character(character)
        return nfa.current_states()

    def rules_for(self, state):
        return [
            FARule(state, c, self.next_state(state, c))
            for c in self._nfa_design._rulebook.alphabet()
        ]

    def discover_states_and_rules(self, states):
        rules = sum([self.rules_for(s) for s in states], [])
        more_states = {frozenset(r.follow()) for r in rules}

        if more_states.issubset(states):
            return (states, rules)
        else:
            return self.discover_states_and_rules(states | more_states)

    def to_dfa_design(self):
        start_state = frozenset(self._nfa_design.to_nfa().current_states())
        states, rules = self.discover_states_and_rules({start_state})
        accept_states = {s for s in states if self._nfa_design.to_nfa(s).accepting()}

        return DFADesign(start_state, accept_states, DFARulebook(rules))
