package dfa;

import java.util.Set;

public class Main {
    public static void main(String[] args) {
        DFARulebook rulebook = new DFARulebook(Set.of(
                new FARule(1, 'a', 2), new FARule(1, 'b', 1),
                new FARule(2, 'a', 2), new FARule(2, 'b', 3),
                new FARule(3, 'a', 3), new FARule(3, 'b', 3)
        ));

        DFADesign dfaDesign = new DFADesign(1, Set.of(3), rulebook);

        System.out.println(dfaDesign.accepts("a"));
        System.out.println(dfaDesign.accepts("b"));
        System.out.println(dfaDesign.accepts("ab"));
        System.out.println(dfaDesign.accepts("abaaaaaabbbababababaabababababab"));
        System.out.println(dfaDesign.accepts("bbbbbaaaaaaaaaaaababababab"));
    }
}
