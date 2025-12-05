from state.state_types import State

def job_analyzer(state: State) -> State:
    job_text = state.get("job_posting", "")
    user_msg = state["messages"][-1].content
    full_context = (job_text + " " + user_msg).lower()

    ai_keywords = ["ai", "machine learning", "deep learning", "python", "nlp", "vision", "gpt"]
    frontend_keywords = ["frontend", "react", "javascript", "typescript", "ui", "ux", "web"]

    is_ai = any(k in full_context for k in ai_keywords)
    is_frontend = any(k in full_context for k in frontend_keywords)

    master = state["master_profile"]
    target_role = "Software Engineer"

    if is_ai and not is_frontend:
        target_role = "AI Engineer"
        skills = master["data"]["ai"]["skills"]
        exp = master["data"]["ai"]["experience"]

    elif is_frontend and not is_ai:
        target_role = "Frontend Developer"
        skills = master["data"]["frontend"]["skills"]
        exp = master["data"]["frontend"]["experience"]

    else:
        target_role = "Full Stack AI Developer"
        skills = master["data"]["ai"]["skills"] + master["data"]["frontend"]["skills"]
        exp = master["data"]["ai"]["experience"] + master["data"]["frontend"]["experience"]

    focused_profile = {
        "name": master["name"],
        "education": master["education"],
        "contact": master["contact"],
        "relevant_skills": skills,
        "relevant_experience": exp,
    }

    return {
        "focused_profile": focused_profile,
        "analysis": {"role": target_role}
    }
