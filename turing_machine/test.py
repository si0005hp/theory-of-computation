import unittest

from dtm import DTM, Tape, TMConfiguration, DTMRulebook, TMRule, DTMDesign


class TestDTM(unittest.TestCase):

    def test_binary_increment(self):
        tape = Tape(['1', '0', '1'], '1', [], '_')
        dtm = DTM(
            TMConfiguration(1, tape), [3],
            DTMRulebook([
                TMRule(1, '0', 2, '1', 'R'),
                TMRule(1, '1', 1, '0', 'L'),
                TMRule(1, '_', 2, '1', 'R'),
                TMRule(2, '0', 2, '0', 'R'),
                TMRule(2, '1', 2, '1', 'R'),
                TMRule(2, '_', 3, '_', 'L')
            ]))

        self.assertFalse(dtm.accepting())
        self.assertEqual(1, dtm.current_configuration.state)
        self.assertEqual('101(1)', str(dtm.current_configuration.tape))

        dtm.run()

        self.assertTrue(dtm.accepting())
        self.assertEqual(3, dtm.current_configuration.state)
        self.assertEqual('110(0)_', str(dtm.current_configuration.tape))

    def test_stuck(self):
        tape = Tape(['1', '2', '1'], '1', [], '_')
        dtm = DTM(TMConfiguration(1, tape), [3], DTMRulebook([]))

        dtm.run()

        self.assertFalse(dtm.accepting())
        self.assertTrue(dtm.is_stuck())

    def test_same_number_of_chars(self):
        tape = Tape([], 'a', ['a', 'a', 'b', 'b', 'b', 'c', 'c', 'c'], '_')
        dtm = DTM(TMConfiguration(1, tape), [6], self._same_number_of_chars_rulebook())

        for _ in range(0, 10):
            dtm.step()
        self.assertFalse(dtm.accepting())
        self.assertEqual(5, dtm.current_configuration.state)
        self.assertEqual('XaaXbbXc(c)_', str(dtm.current_configuration.tape))

        for _ in range(0, 25):
            dtm.step()
        self.assertFalse(dtm.accepting())
        self.assertEqual(5, dtm.current_configuration.state)
        self.assertEqual('_XXa(X)XbXXc_', str(dtm.current_configuration.tape))

        dtm.run()
        self.assertTrue(dtm.accepting())
        self.assertEqual(6, dtm.current_configuration.state)
        self.assertEqual('_XXXXXXXX(X)_', str(dtm.current_configuration.tape))

    def _same_number_of_chars_rulebook(self):
        return DTMRulebook([
            # state1: scan to the right, searching for a
            TMRule(1, 'X', 1, 'X', 'R'),  # skip X
            TMRule(1, 'a', 2, 'X', 'R'),  # replace a to X, move to state2
            TMRule(1, '_', 6, '_', 'L'),  # found space, move to state6 (accept)

            # state2: scan to the right, searching for b
            TMRule(2, 'a', 2, 'a', 'R'),  # skip a
            TMRule(2, 'X', 2, 'X', 'R'),  # skip X
            TMRule(2, 'b', 3, 'X', 'R'),  # replace b to X, move to state3

            # state3: scan to the right, searching for c
            TMRule(3, 'b', 3, 'b', 'R'),  # skip b
            TMRule(3, 'X', 3, 'X', 'R'),  # skip X
            TMRule(3, 'c', 4, 'X', 'R'),  # replace c to X, move to state4

            # state4: scan to the right, searching for c
            TMRule(4, 'c', 4, 'c', 'R'),  # skip c
            TMRule(4, '_', 5, '_', 'L'),  # found space, move to state5

            # state5: scan to the left, searching for the head of characters
            TMRule(5, 'a', 5, 'a', 'L'),  # skip a
            TMRule(5, 'b', 5, 'b', 'L'),  # skip b
            TMRule(5, 'c', 5, 'c', 'L'),  # skip c
            TMRule(5, 'X', 5, 'X', 'L'),  # skip X
            TMRule(5, '_', 1, '_', 'R'),  # found space, move to state1
        ])

    def test_dtm_design(self):

        def make_tape(string):
            if len(string) < 1:
                return Tape([], '_', [], '_')
            return Tape([], string[0], [c for c in string[1:]], '_')

        dtm_design = DTMDesign(1, [6], self._same_number_of_chars_rulebook())

        dtm_design.draw()

        for string in ["", "abc", "aaabbbccc"]:
            self.assertTrue(dtm_design.accepts(make_tape(string)))

        for string in ["a", "ab", "ac", "bc", "abcc"]:
            self.assertFalse(dtm_design.accepts(make_tape(string)))


if __name__ == '__main__':
    unittest.main()
