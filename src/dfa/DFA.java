package dfa;

import java.util.Set;

public class DFA {
    int currentState;
    Set<Integer> acceptStates;
    DFARulebook rulebook;

    public DFA(int currentState, Set<Integer> acceptStates, DFARulebook rulebook) {
        this.currentState = currentState;
        this.acceptStates = acceptStates;
        this.rulebook = rulebook;
    }

    public boolean accepting() {
        return acceptStates.contains(currentState);
    }

    public void readCharacter(char character) {
        this.currentState = rulebook.nextState(currentState, character);
    }

    public void readString(String str) {
        str.chars().forEach(c -> readCharacter((char)c));
    }
}
