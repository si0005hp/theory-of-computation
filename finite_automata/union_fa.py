import dfa

dfa1 = dfa.DFADesign(
    1, {3}, dfa.DFARulebook([
        dfa.FARule(1, 'a', 2),
        dfa.FARule(2, 'a', 3),
        dfa.FARule(3, 'a', 2),
    ]))

dfa2 = dfa.DFADesign(
    1, {4},
    dfa.DFARulebook([
        dfa.FARule(1, 'a', 2),
        dfa.FARule(2, 'a', 3),
        dfa.FARule(3, 'a', 4),
        dfa.FARule(4, 'a', 5),
        dfa.FARule(5, 'a', 3),
    ]))


def all_dfa_states(dfa):
    return set(sum([[r._state, r._next_state] for r in dfa._rulebook._rules], []))


def next_dfa_state(dfa, state, character):
    return dfa._rulebook.next_state(state, character)


start_state = (dfa1._start_state, dfa2._start_state)
all_states = [(a, b) for a in all_dfa_states(dfa1) for b in all_dfa_states(dfa2)]
accept_states = [
    s for s in all_states if s[0] in dfa1._accept_states or s[1] in dfa2._accept_states
]

char = 'a'
rules = [
    dfa.FARule(s, char, (next_dfa_state(dfa1, s[0], char), next_dfa_state(dfa2, s[1], char)))
    for s in all_states
]

union_fa = dfa.DFADesign(start_state, accept_states, dfa.DFARulebook(rules))

dfa1.draw()
dfa2.draw()
union_fa.draw()
