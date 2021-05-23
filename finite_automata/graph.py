# -*- coding: utf-8 -*-
import graphviz
import fa_util


class Graph:

    def draw(self, directory, filename, rules, start_state, accept_states):
        g = graphviz.Digraph(format="svg", graph_attr={'rankdir': 'LR'})
        self.add_start_edge(g, start_state)

        edges = {}
        for rule in rules:
            from_state = self.state_to_str(self.get_state(rule))
            to_state = self.state_to_str(self.get_next_state(rule))

            self.add_graph_node(g, self.get_state(rule), from_state, accept_states)
            self.add_graph_node(g, self.get_next_state(rule), to_state, accept_states)

            label = self.make_label(rule)
            edge_labels = edges.get((from_state, to_state))
            if edge_labels == None:
                edges[(from_state, to_state)] = [label]
            else:
                edge_labels.append(label)
        self.add_edges(g, edges)

        g.render(filename=filename, directory=directory, format="png", view=True)

    # Supposed to be extended
    def make_label(self, rule):
        return "ε" if rule._character == None else rule._character

    # Supposed to be extended
    def format_labels(self, labels):
        return ','.join(labels)

    # Supposed to be extended
    def get_state(self, rule):
        return rule._state

    # Supposed to be extended
    def get_next_state(self, rule):
        return rule._next_state

    def add_start_edge(self, graph, start_state):
        dummy_node = fa_util.random_str(8)
        graph.node(dummy_node, style="invis", shape="point")
        graph.edge(dummy_node, self.state_to_str(start_state), style="bold")

    def add_graph_node(self, graph, state, state_str, accept_states):
        attr = {'root': 'true', 'shape': 'circle'}
        if state in accept_states:
            attr['shape'] = 'doublecircle'
        graph.node(state_str, **attr)

    def add_edges(self, graph, edges):
        for (_from, to), labels in edges.items():
            graph.edge(_from, to, self.format_labels(labels))

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
