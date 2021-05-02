import unittest

from npda import NPDARulebook, NPDA, NPDADesign, PDARule
from lexical_analyzer import LexicalAnalyzer

##################
# SIMPLE grammar
##################
# <statement>  ::=  <while> | <assign>
# <while>      ::=  'w' '(' <expression> ')' '{' <statement> '}'
# <assign>     ::=  'v' '=' <expression>
# <expression> ::=  <less-than>
# <less-than>  ::=  <multiply> '<' <less-than> | <multiply>
# <multiply>   ::=  <term> ' * ' <multiply> | <term>
# <term>       ::=  'n' | 'v'


class TestCFGPDAConversion(unittest.TestCase):

    def test_cfg_pda_conversion(self):
        npda_design = self.convert_cfg_to_pda()

        self.assertTrue(npda_design.accepts(self.lex('while (x < 5) { x = x * 3 }')))
        self.assertFalse(npda_design.accepts(self.lex('while (x < 5 x = x * }')))

    def convert_cfg_to_pda(self):
        start_rule = PDARule(1, None, 2, '$', ['S', '$'])

        symbol_rules = [
            # <statement> ::= <while> | <assign>
            PDARule(2, None, 2, 'S', ['W']),
            PDARule(2, None, 2, 'S', ['A']),
            # <while> ::= 'w' '(' <expression> ')' '{' <statement> '}'
            PDARule(2, None, 2, 'W', ['w', '(', 'E', ')', '{', 'S', '}']),
            # <assign> ::= 'v' '=' <expression>
            PDARule(2, None, 2, 'A', ['v', '=', 'E']),
            # <expression> ::= <less-than>
            PDARule(2, None, 2, 'E', ['L']),
            # <less-than> ::= <multiply> '<' <less-than> | <multiply>
            PDARule(2, None, 2, 'L', ['M', '<', 'L']),
            PDARule(2, None, 2, 'L', ['M']),
            # <multiply> ::= <term> '*' <multiply> | <term>
            PDARule(2, None, 2, 'M', ['T', '*', 'M']),
            PDARule(2, None, 2, 'M', ['T']),
            # <term> ::= 'n' | 'v'
            PDARule(2, None, 2, 'T', ['n']),
            PDARule(2, None, 2, 'T', ['v'])
        ]

        token_rules = [
            PDARule(2, rule['token'], 2, rule['token'], []) for rule in LexicalAnalyzer.GRAMMAR
        ]

        stop_rule = PDARule(2, None, 3, '$', ['$'])

        rulebook = NPDARulebook([start_rule, stop_rule] + symbol_rules + token_rules)
        return NPDADesign(1, '$', [3], rulebook)

    def lex(self, string):
        return ''.join(LexicalAnalyzer(string).analyze())


if __name__ == "__main__":
    unittest.main()
