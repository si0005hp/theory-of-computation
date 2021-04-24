package dfa;

import java.util.Set;

public class DFARulebook {
    Set<FARule> rules;

    public DFARulebook(Set<FARule> rules) {
        this.rules = rules;
    }

    public int nextState(int state, char character) {
        return ruleFor(state, character).follow();
    }

    public FARule ruleFor(int state, char character) {
        return rules.stream()
                .filter(rule -> rule.appliesTo(state, character))
                .findFirst()
                .get();
    }
}
