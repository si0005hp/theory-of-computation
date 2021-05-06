import unittest

from rexp import Literal, Empty, Choose, Concatenate, Repeat


class Test(unittest.TestCase):

    def test_literal(self):
        self.assertTrue(Literal('a').matches('a'))
        self.assertFalse(Literal('a').matches('b'))
        self.assertFalse(Literal('a').matches('aa'))

    def test_empty(self):
        self.assertTrue(Empty().matches(''))
        self.assertFalse(Empty().matches('a'))

    def test_choose(self):
        choose = Choose(Literal('a'), Literal('b'))

        self.assertEqual('a|b', str(choose))
        for s in ['a', 'b']:
            self.assertTrue(choose.matches(s))
        for s in ['', 'c', 'aa', 'bb', 'ab']:
            self.assertFalse(choose.matches(s))

    def test_concatenate(self):
        concat = Concatenate(Literal('a'), Literal('b'))

        self.assertEqual('ab', str(concat))
        self.assertTrue(concat.matches('ab'))
        for s in ['', 'a', 'b', 'c', 'aa', 'bb', 'aba', 'bab']:
            self.assertFalse(concat.matches(s))

    def test_repeat(self):
        repeat = Repeat(Literal('a'))

        self.assertEqual('a*', str(repeat))
        for s in ['', 'a', 'aa', 'aaa', 'aaaa']:
            self.assertTrue(repeat.matches(s))
        for s in ['b', 'ab', 'aab', 'ba']:
            self.assertFalse(repeat.matches(s))

    def test_precedence(self):
        self.assertEqual('ab*', str(Concatenate(Literal('a'), Repeat(Literal('b')))))
        self.assertEqual('(ab)*', str(Repeat(Concatenate(Literal('a'), Literal('b')))))
        self.assertEqual('(a|b)*', str(Repeat(Choose(Literal('a'), Literal('b')))))


if __name__ == '__main__':
    unittest.main()
