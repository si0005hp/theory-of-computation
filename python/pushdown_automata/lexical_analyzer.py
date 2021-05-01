import re


class LexicalAnalyzer:
    GRAMMAR = [{
        'token': 'i',
        'pattern': r'if'
    }, {
        'token': 'e',
        'pattern': r'else'
    }, {
        'token': 'w',
        'pattern': r'while'
    }, {
        'token': 'd',
        'pattern': r'do-nothing'
    }, {
        'token': '(',
        'pattern': r'\('
    }, {
        'token': ')',
        'pattern': r'\)'
    }, {
        'token': '{',
        'pattern': r'\{'
    }, {
        'token': '}',
        'pattern': r'\}'
    }, {
        'token': ';',
        'pattern': r';'
    }, {
        'token': '=',
        'pattern': r'='
    }, {
        'token': '+',
        'pattern': r'\+'
    }, {
        'token': '*',
        'pattern': r'\*'
    }, {
        'token': '<',
        'pattern': r'<'
    }, {
        'token': 'n',
        'pattern': r'[0-9]+'
    }, {
        'token': 'b',
        'pattern': r'true|false'
    }, {
        'token': 'v',
        'pattern': r'[a-z]+'
    }]

    def __init__(self, string):
        self._string = string

    def analyze(self):
        tokens = []
        while self.has_more_tokens():
            tokens.append(self.next_token())
        return tokens

    def has_more_tokens(self):
        return len(self._string) > 0

    def next_token(self):
        rule, match = self.rule_matching(self._string)
        self._string = self.string_after(match)
        return rule['token']

    def rule_matching(self, string):
        matches = [re.search(r'\A' + g['pattern'], string) for g in self.GRAMMAR]
        rules_with_matches = [[g, m] for g, m in zip(self.GRAMMAR, matches) if m != None]
        return max(rules_with_matches, key=lambda gm: gm[1].span()[1] - gm[1].span()[0])

    def string_after(self, match):
        return match.string[match.end():].lstrip()
