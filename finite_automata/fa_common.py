# -*- coding: utf-8 -*-
import graphviz
import util


class FARule:

    def __init__(self, state, character, next_state):
        self._state = state
        self._character = character
        self._next_state = next_state

    def applies_to(self, state, character):
        return self._state == state and self._character == character

    def follow(self):
        return self._next_state

    def __repr__(self):
        return '{} --{}--> {}'.format(self._state, self._character, self._next_state)


class FADesign:

    def __init__(self, start_state, accept_states, rulebook):
        self._start_state = start_state
        self._accept_states = accept_states
        self._rulebook = rulebook

    def draw(self, directory=None, filename=None):
        if directory == None:
            directory = "/tmp"
        if filename == None:
            filename = util.random_str(8)

        self.draw_graph(directory, filename, self._rulebook._rules, self._start_state,
                        self._accept_states)

    def draw_graph(self, directory, filename, rules, start_state, accept_states):
        g = graphviz.Digraph(format="svg", graph_attr={'rankdir': 'LR'})
        self.add_start_edge(g, start_state)

        edges = {}
        for rule in rules:
            from_state = self.state_to_str(rule._state)
            to_state = self.state_to_str(rule._next_state)

            self.add_graph_node(g, rule._state, from_state, accept_states)
            self.add_graph_node(g, rule._next_state, to_state, accept_states)

            label = "ε" if rule._character == None else rule._character
            edge_labels = edges.get((from_state, to_state))
            if edge_labels == None:
                edges[(from_state, to_state)] = [label]
            else:
                edge_labels.append(label)
        self.add_edges(g, edges)

        g.render(filename=filename, directory=directory, format="png", view=True)

    def add_start_edge(self, graph, start_state):
        dummy_node = util.random_str(8)
        graph.node(dummy_node, style="invis", shape="point")
        graph.edge(dummy_node, self.state_to_str(start_state), style="bold")

    def add_graph_node(self, graph, state, state_str, accept_states):
        attr = {'root': 'true', 'shape': 'circle'}
        if state in accept_states:
            attr['shape'] = 'doublecircle'
        graph.node(state_str, **attr)

    def add_edges(self, graph, edges):
        for (_from, to), labels in edges.items():
            graph.edge(_from, to, ','.join(labels))

    def state_to_str(self, state):
        if isinstance(state, str):
            return state

        try:
            iter(state)
            ### state is iterable ###
            if len(state) == 0:
                return 'Ø'

            # converting list object directly to set object break the order of elements in string
            list_str = str([self.state_to_str(e) for e in sorted(state)])
            return list_str.replace('[', '{').replace(']', '}')
        except TypeError:
            ### state is not iterable ###
            return str(state)
