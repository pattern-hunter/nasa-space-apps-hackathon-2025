from langgraph.graph import START, StateGraph
from langgraph.graph.state import CompiledStateGraph
import classes as cls
import steps
from datetime import datetime

# TODO: human-in-the-loop
def build_graph():
    graph_builder = StateGraph(cls.State).add_sequence(
        [steps.write_query, steps.execute_query, steps.generate_answer]
    )
    graph_builder.add_edge(START, "write_query")
    graph = graph_builder.compile()
    return graph

def execute_graph(graph: CompiledStateGraph, state: cls.State) -> cls.State:
    for step in graph.stream(state, stream_mode="updates"):
        if "generate_answer" in step:
            state = step["generate_answer"]

    return state