import collections

class TuringMachine:
    def __init__(
            self,
            transition_function={},
            initial_state='q_s',
            blank_symbol='[]',
            head_movements={-1: ('<-', '<'), 0: ('-', '.'), 1: ('->', '>')},
            symbols_representations={'[]': '□'},
            empty_word_representation='ε',
            #head_representation='^',
            step_limit=1_000_000
        ):
        self.transition_function, self.initial_state, self.blank_symbol, self.symbols_representations, self.empty_word_representation, self.step_limit = \
            transition_function, initial_state, blank_symbol, symbols_representations, empty_word_representation, step_limit
        self.head_movements = {arrow: delta for delta, arrows in head_movements.items() for arrow in arrows}

        self.states = self.transition_function.keys()
        self.symbols = set(symbol for values in self.transition_function.values() for symbol in values.keys())
        self.arrows = self.head_movements.keys()

        assert self.states.isdisjoint(self.symbols)
        assert self.states.isdisjoint(self.arrows)
        assert self.symbols.isdisjoint(self.arrows)

        self.used_states_and_symbols = set()

    def parse_sequence(self, sequence):        
        if sequence is None:
            return []
        if isinstance(sequence, str):
            return list(sequence)
        return sequence

    def format_sequence(self, sequence):
        if not sequence and self.empty_word_representation:
            return self.empty_word_representation
        return '"' + ''.join((
            self.symbols_representations.get(symbol, symbol)
            for symbol in sequence
        )) + '"'
        
    def execute(self, input_sequence=None):
        tape = collections.defaultdict(lambda: self.blank_symbol, enumerate(self.parse_sequence(input_sequence)))
        state, head_position = self.initial_state, 0

        for i in range(self.step_limit):
            #print(head_position, state, ''.join(tape.values()))  

            symbol = tape[head_position]
            """
            if (state, symbol) in self.transition_function:
                value = self.transition_function[(state, symbol)]
            elif (symbol, state) in self.transition_function:
                value = self.transition_function[(symbol, state)]
            elif symbol in self.transition_function and state in self.transition_function[symbol]:
                value = self.transition_function[symbol][state]
            el"""
            if state in self.transition_function and symbol in self.transition_function[state]:
                value = self.transition_function[state][symbol]
            else:
                raise ValueError(f'Transition function not defined for state {state} and symbol {symbol}')
            self.used_states_and_symbols.add((state, symbol))

            if value in (True, False):
                return value # todo: also return tape

            if not isinstance(value, tuple):
                value = (value,)

            new_symbol, new_state, arrow = None, None, None
            for v in value:
                if new_symbol is None and v in self.symbols:
                    new_symbol = v
                elif new_state is None and v in self.states:
                    new_state = v
                elif arrow is None and v in self.arrows:
                    arrow = v
                else:
                    raise ValueError(f'Invalid transition function value {v} for state {state} and symbol {symbol}')

            if new_symbol is not None:
                tape[head_position] = new_symbol
            if new_state is not None:
                state = new_state
            if arrow is not None:
                head_position += self.head_movements[arrow]
                #if head_position < 0:
                #    head_position = 0
        else:
            raise ValueError(f'Step limit of {self.step_limit} has been exceeded for input sequence {self.format_sequence(input_sequence)}')

    def run_tests(self, test_cases=None, inputs=None, expected_func=None):
        if test_cases is not None:
            tests = test_cases.items()
        elif inputs is not None and expected_func is not None:
            tests = ((word, expected_func(word)) for word in inputs)
        else:
            raise ValueError('Either test cases or both inputs and expected function must be supplied')

        for input_sequence, expected in tests:
            actual = self.execute(input_sequence)
            passed = (actual == expected)
            print(f'{self.format_sequence(input_sequence)}: {"Passed" if passed else "Failed"}')
            if not passed:
                return False

        print('All tests passed')
        for state, values in self.transition_function.items():
            for symbol in values.keys():
                if (state, symbol) not in self.used_states_and_symbols:
                    print(f'Transition for ({state}, {symbol}) was redundant for supplied test cases')
        return True
