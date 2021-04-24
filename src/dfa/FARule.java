package dfa;

import java.util.Objects;

public class FARule {
    int state;
    char character;
    int nextState;

    public FARule(int state, char character, int nextState) {
        this.state = state;
        this.character = character;
        this.nextState = nextState;
    }

    public boolean appliesTo(int state, char character) {
        return this.state == state && this.character == character;
    }

    public int follow() {
        return nextState;
    }

    @Override
    public String toString() {
        return String.format("%s --%s--> %s", state, character, nextState);
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        FARule faRule = (FARule) o;
        return state == faRule.state && character == faRule.character && nextState == faRule.nextState;
    }

    @Override
    public int hashCode() {
        return Objects.hash(state, character, nextState);
    }
}
