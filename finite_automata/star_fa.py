import dfa
import nfa

dfa = dfa.DFADesign(
    'x1', {'x3'},
    dfa.DFARulebook([
        dfa.FARule('x1', 'a', 'x2'),
        dfa.FARule('x2', 'a', 'x2'),
        dfa.FARule('x2', 'b', 'x2'),
        dfa.FARule('x2', 'c', 'x3'),
    ]))

start_state = 'dummy'
accept_states = dfa._accept_states | {start_state}

start_rule = nfa.FARule(start_state, None, dfa._start_state)
rewind_rules = [nfa.FARule(s, None, dfa._start_state) for s in dfa._accept_states]
rules = dfa._rulebook._rules + [start_rule] + rewind_rules

star_fa = nfa.NFADesign(start_state, accept_states, nfa.NFARulebook(rules))
star_fa.draw()
