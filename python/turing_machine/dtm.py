class Tape:

    def __init__(self, left, middle, right, blank):
        self.left = left
        self.middle = middle
        self.right = right
        self.blank = blank

    def __str__(self):
        return "{}({}){}".format(''.join(self.left), self.middle, ''.join(self.right))

    def __repr__(self):
        return "<Tape {}>".format(self.__str__())

    def write(self, character):
        return Tape(self.left, character, self.right, self.blank)

    def move_head_left(self):
        return Tape(
            self.left[:-1],
            self.left[-1] if len(self.left) > 0 else self.blank,
            [self.middle, *self.right],
            self.blank,
        )

    def move_head_right(self):
        return Tape(
            [*self.left, self.middle],
            self.right[0] if len(self.right) > 0 else self.blank,
            self.right[1:],
            self.blank,
        )


class TMConfiguration:

    def __init__(self, state, tape):
        self.state = state
        self.tape = tape

    def __repr__(self):
        return '<state: {}, tape: {}>'.format(self.state, self.tape)


class TMRule:

    def __init__(self, state, character, next_state, write_character, direction):
        self.state = state
        self.character = character
        self.next_state = next_state
        self.write_character = write_character
        self.direction = direction

    def applies_to(self, configuration):
        return self.state == configuration.state and self.character == configuration.tape.middle

    def follow(self, configuration):
        return TMConfiguration(self.next_state, self.next_tape(configuration))

    def next_tape(self, configuration):
        written_tape = configuration.tape.write(self.write_character)

        if self.direction == 'L':
            return written_tape.move_head_left()
        elif self.direction == 'R':
            return written_tape.move_head_right()


class DTMRulebook:

    def __init__(self, rules):
        self.rules = rules

    def rule_for(self, configuration):
        matched_rules = [r for r in self.rules if r.applies_to(configuration)]
        return None if len(matched_rules) == 0 else next(iter(matched_rules))

    def applies_to(self, configuration):
        return self.rule_for(configuration) != None

    def next_configuration(self, configuration):
        return self.rule_for(configuration).follow(configuration)


class DTM:

    def __init__(self, current_configuration, accept_states, rulebook):
        self.current_configuration = current_configuration
        self.accept_states = accept_states
        self.rulebook = rulebook

    def accepting(self):
        return self.current_configuration.state in self.accept_states

    def step(self):
        self.current_configuration = self.rulebook.next_configuration(self.current_configuration)

    def run(self):
        while not self.accepting() and not self.is_stuck():
            self.step()

    def is_stuck(self):
        return not self.accepting() and not self.rulebook.applies_to(self.current_configuration)