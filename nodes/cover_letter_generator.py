from langchain_core.prompts import ChatPromptTemplate
from llm.ollama_client import llm

def cover_letter_generator(state):
    prompt = ChatPromptTemplate.from_template(
        "Write a cover letter for a {role}.\n"
        "Use ONLY the following info:\n{profile}\n"
        "Job Description: {job}\n"
    )

    output = (prompt | llm).invoke({
        "profile": state["focused_profile"],
        "role": state["analysis"]["role"],
        "job": state.get("job_posting", "")
    }).content

    return {"cover_letter": output}
