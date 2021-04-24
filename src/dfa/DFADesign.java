package dfa;

import java.util.Set;

public class DFADesign {
    int startState;
    Set<Integer> acceptStates;
    DFARulebook rulebook;

    public DFADesign(int startState, Set<Integer> acceptStates, DFARulebook rulebook) {
        this.startState = startState;
        this.acceptStates = acceptStates;
        this.rulebook = rulebook;
    }

    public boolean accepts(String str) {
        DFA dfa = new DFA(startState, acceptStates, rulebook);
        dfa.readString(str);
        return dfa.accepting();
    }
}
