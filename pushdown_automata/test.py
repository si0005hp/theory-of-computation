import unittest
import os

from dpda import DPDARulebook, DPDA, DPDADesign
from npda import NPDARulebook, NPDA, NPDADesign
from pda_common import PDARule, PDAConfiguration, Stack


class TestBase(unittest.TestCase):

    def draw(self, design, test_case_name):
        filename = "{}_{}".format(self.__class__.__name__, test_case_name)
        use_label_simple = os.environ.get("SIMPLE_GRAPH") == "1"
        if use_label_simple:
            filename = filename + "_simple"
        design.draw("/tmp", filename, use_label_simple)


class TestStack(TestBase):

    def test_stack(self):
        self.assertEqual('a', Stack().push('a').__str__())
        self.assertEqual('aa', Stack().push('a').push('a').__str__())
        self.assertEqual('', Stack().push('a').pop().__str__())
        self.assertEqual('a', Stack().push('a').top())
        self.assertEqual('aaa', Stack(['a', 'a', 'a']).__str__())


class TestDPDA(TestBase):

    def test_dpda(self):
        design = DPDADesign(
            1, '$', [1],
            DPDARulebook([
                PDARule(1, '(', 2, '$', ['b', '$']),
                PDARule(2, '(', 2, 'b', ['b', 'b']),
                PDARule(2, ')', 2, 'b', []),
                PDARule(2, None, 1, '$', ['$'])
            ]))

        super().draw(design, 'test_dpda')

        for string in ['(', ')', '()(', '(()', '(()(()(()()(()()))()']:
            self.assertFalse(design.accepts(string))

        for string in ['', '()', '(())', '()()', '(()(()))', '()(())((()))(()(()))']:
            self.assertTrue(design.accepts(string))

    def test_dpda2(self):
        design = DPDADesign(
            1, '$', [3],
            DPDARulebook([
                PDARule(1, 'a', 1, '$', ['a', '$']),
                PDARule(1, 'a', 1, 'a', ['a', 'a']),
                PDARule(1, 'a', 1, 'b', ['a', 'b']),
                PDARule(1, 'b', 1, '$', ['b', '$']),
                PDARule(1, 'b', 1, 'a', ['b', 'a']),
                PDARule(1, 'b', 1, 'b', ['b', 'b']),
                PDARule(1, 'm', 2, '$', ['$']),
                PDARule(1, 'm', 2, 'a', ['a']),
                PDARule(1, 'm', 2, 'b', ['b']),
                PDARule(2, 'a', 2, 'a', []),
                PDARule(2, 'b', 2, 'b', []),
                PDARule(2, None, 3, '$', ['$'])
            ]))

        super().draw(design, 'test_dpda2')

        for string in ['abmb', 'baambaa']:
            self.assertFalse(design.accepts(string))

        for string in ['ama', 'babbamabbab']:
            self.assertTrue(design.accepts(string))


class TestNPDA(TestBase):

    def test_npda(self):
        design = NPDADesign(
            1, '$', [3],
            NPDARulebook([
                PDARule(1, 'a', 1, '$', ['a', '$']),
                PDARule(1, 'a', 1, 'a', ['a', 'a']),
                PDARule(1, 'a', 1, 'b', ['a', 'b']),
                PDARule(1, 'b', 1, '$', ['b', '$']),
                PDARule(1, 'b', 1, 'a', ['b', 'a']),
                PDARule(1, 'b', 1, 'b', ['b', 'b']),
                PDARule(1, None, 2, '$', ['$']),
                PDARule(1, None, 2, 'a', ['a']),
                PDARule(1, None, 2, 'b', ['b']),
                PDARule(2, 'a', 2, 'a', []),
                PDARule(2, 'b', 2, 'b', []),
                PDARule(2, None, 3, '$', [])
            ]))

        super().draw(design, 'test_npda')

        for string in ['a', 'ab', 'abb', 'baabaa']:
            self.assertFalse(design.accepts(string))

        for string in ['aa', 'abba', 'babbaabbab']:
            self.assertTrue(design.accepts(string))


if __name__ == '__main__':
    unittest.main()
