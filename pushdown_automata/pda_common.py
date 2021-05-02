from functools import reduce


class Stack:

    def __init__(self, contents=None):
        self._contents = [] if contents == None else contents

    def push(self, character):
        return Stack(self._contents + [character])

    def pop(self):
        return Stack(self._contents[:-1])

    def top(self):
        return self._contents[-1]

    def __str__(self):
        return ''.join(self._contents)

    def __repr__(self):
        return self.__str__()


class PDAConfiguration:
    STUCK_STATE = object()

    def __init__(self, state, stack):
        self.state = state
        self.stack = stack

    def stuck(self):
        return PDAConfiguration(self.STUCK_STATE, self.stack)

    def is_stuck(self):
        return self.state == self.STUCK_STATE

    def __hash__(self):
        return hash(self.__str__())

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __str__(self):
        return '<state: {}, stack: {}>'.format('stucked' if self.is_stuck() else self.state,
                                               self.stack)

    def __repr__(self):
        return self.__str__()


class PDARule:

    def __init__(self, state, character, next_state, pop_character, push_characters):
        self._state = state
        self._character = character
        self._next_state = next_state
        self._pop_character = pop_character
        self._push_characters = push_characters

    def applies_to(self, configuration, character):
        return self._state == configuration.state and self._pop_character == configuration.stack.top(
        ) and self._character == character

    def follow(self, configuration):
        return PDAConfiguration(self._next_state, self.next_stack(configuration))

    def next_stack(self, configuration):
        popped_stack = configuration.stack.pop()
        return reduce(lambda stack, c: stack.push(c), reversed(self._push_characters), popped_stack)
