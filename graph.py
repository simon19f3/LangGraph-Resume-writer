from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from state.state_types import State

from nodes.profile_collector import profile_collector
from nodes.job_analyzer import job_analyzer
from nodes.routing import route_request
from nodes.resume_generator import resume_generator
from nodes.cover_letter_generator import cover_letter_generator
from nodes.screening_generator import screening_generator


def build_graph():
    graph = StateGraph(State)

    graph.add_node("profile_collector", profile_collector)
    graph.add_node("job_analyzer", job_analyzer)
    graph.add_node("resume_generator", resume_generator)
    graph.add_node("cover_letter_generator", cover_letter_generator)
    graph.add_node("screening_generator", screening_generator)

    graph.add_edge(START, "profile_collector")
    graph.add_edge("profile_collector", "job_analyzer")
    graph.add_conditional_edges("job_analyzer", route_request)

    graph.add_edge("resume_generator", END)
    graph.add_edge("cover_letter_generator", END)
    graph.add_edge("screening_generator", END)

    memory = MemorySaver()
    return graph.compile(checkpointer=memory)
