from pythomata import SimpleDFA
alphabet = {"a", "b"}
states = {"s1", "s2", "s3"}

initial_state = "s1"
accepting_states = {"s3"}
transition_function = {"s1": {"b": "s1", "a": "s2"}, "s2": {"a": "s2", "b": "s3"}, "s3": {"a": "s3", "b": "s3"}}

dfa = SimpleDFA(states, alphabet, initial_state, accepting_states, transition_function)

# g = dfa.minimize().trim().to_graphviz()
g = dfa.to_graphviz()
g.render(filename="dfa", directory="/tmp", format="png", view=True)
