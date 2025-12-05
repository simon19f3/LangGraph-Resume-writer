from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]
    master_profile: dict
    focused_profile: dict
    job_posting: str
    analysis: dict
    resume: str
    cover_letter: str
    screening_answers: str
