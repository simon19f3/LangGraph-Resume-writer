from langchain_core.prompts import ChatPromptTemplate
from llm.ollama_client import llm

def screening_generator(state):
    prompt = ChatPromptTemplate.from_template(
        "Act as an interviewer for a {role}.\n"
        "Based on my skills: {profile}\n"
        "Ask 3 technical questions and provide ideal answers."
    )

    output = (prompt | llm).invoke({
        "profile": state["focused_profile"],
        "role": state["analysis"]["role"],
    }).content

    return {"screening_answers": output}
