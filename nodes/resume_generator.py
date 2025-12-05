from langchain_core.prompts import ChatPromptTemplate
from llm.ollama_client import llm

def resume_generator(state):
    prompt = ChatPromptTemplate.from_template(
        "Write a resume for a {role}.\n"
        "Use ONLY this data:\n{profile}\n"
        "Job Description: {job}\n"
        "Format: Markdown."
    )

    output = (prompt | llm).invoke({
        "profile": state["focused_profile"],
        "role": state["analysis"]["role"],
        "job": state.get("job_posting", "")
    }).content

    return {"resume": output}
