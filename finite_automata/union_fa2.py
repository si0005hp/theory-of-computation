import dfa
import nfa

dfa1 = dfa.DFADesign(
    'x1', {'x3'},
    dfa.DFARulebook([
        dfa.FARule('x1', 'a', 'x2'),
        dfa.FARule('x2', 'a', 'x3'),
        dfa.FARule('x3', 'a', 'x2'),
    ]))

dfa2 = dfa.DFADesign(
    'y1', {'y4'},
    dfa.DFARulebook([
        dfa.FARule('y1', 'b', 'y2'),
        dfa.FARule('y2', 'b', 'y3'),
        dfa.FARule('y3', 'b', 'y4'),
        dfa.FARule('y4', 'b', 'y5'),
        dfa.FARule('y5', 'b', 'y3'),
    ]))

start_state = 'dummy'
accept_states = dfa1._accept_states | dfa2._accept_states

start_rules = [nfa.FARule(start_state, None, s) for s in [dfa1._start_state, dfa2._start_state]]
rules = dfa1._rulebook._rules + dfa2._rulebook._rules + start_rules

union_fa2 = nfa.NFADesign(start_state, accept_states, nfa.NFARulebook(rules))
union_fa2.draw()
