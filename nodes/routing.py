def route_request(state):
    text = state["messages"][-1].content.lower()

    if "cover" in text:
        return "cover_letter_generator"

    if any(w in text for w in ["screen", "interview", "question"]):
        return "screening_generator"

    return "resume_generator"
