import unittest

from dfa import DFARulebook, FARule, DFADesign
from nfa import NFARulebook, NFADesign
from nfa_simulation import NFASimulation


class TestDFA(unittest.TestCase):

    def test_dfa(self):
        design = DFADesign(
            1, {3},
            DFARulebook([
                FARule(1, 'a', 2),
                FARule(1, 'b', 1),
                FARule(2, 'a', 2),
                FARule(2, 'b', 3),
                FARule(3, 'a', 3),
                FARule(3, 'b', 3),
            ]))

        for string in ["b", "bb", "a", "ba", "aa", "bbaaa"]:
            self.assertFalse(design.accepts(string))

        for string in ["ab", "bab", "bbaaab", "abbaba"]:
            self.assertTrue(design.accepts(string))


class TestNFA(unittest.TestCase):

    def test_nfa(self):
        design = NFADesign(
            1, {2, 4},
            NFARulebook([
                FARule(1, None, 2),
                FARule(1, None, 4),
                FARule(2, 'a', 3),
                FARule(3, 'a', 2),
                FARule(4, 'a', 5),
                FARule(5, 'a', 6),
                FARule(6, 'a', 4),
            ]))

        for string in ["a", "aaaaa", "aaaaaaa"]:
            self.assertFalse(design.accepts(string))

        for string in ["aa", "aaa", "aaaa", "aaaaaa", "aaaaaaaa"]:
            self.assertTrue(design.accepts(string))


class TestNFA(unittest.TestCase):

    def test_nfa(self):
        design = NFADesign(
            1, {2, 4},
            NFARulebook([
                FARule(1, None, 2),
                FARule(1, None, 4),
                FARule(2, 'a', 3),
                FARule(3, 'a', 2),
                FARule(4, 'a', 5),
                FARule(5, 'a', 6),
                FARule(6, 'a', 4),
            ]))

        for string in ["a", "aaaaa", "aaaaaaa"]:
            self.assertFalse(design.accepts(string))

        for string in ["aa", "aaa", "aaaa", "aaaaaa", "aaaaaaaa"]:
            self.assertTrue(design.accepts(string))


class TestNFASimulation(unittest.TestCase):

    def test_nfa_simulation(self):
        nfa_design = NFADesign(
            1, {3},
            NFARulebook([
                FARule(1, 'a', 1),
                FARule(1, 'a', 2),
                FARule(1, None, 2),
                FARule(2, 'b', 3),
                FARule(3, 'b', 1),
                FARule(3, None, 2),
            ]))
        simulation = NFASimulation(nfa_design)
        dfa_design = simulation.to_dfa_design()

        for string in ["a", "aa", "abab"]:
            self.assertFalse(dfa_design.accepts(string))

        for string in ["b", "ab", "bb", "bbb", "aabbbbbaab"]:
            self.assertTrue(dfa_design.accepts(string))


if __name__ == "__main__":
    unittest.main()
