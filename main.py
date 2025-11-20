from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
import gradio as gr

# ==================== LLM CONFIGURATION ====================
# Ensure you have Ollama running: `ollama run llama3.2`
llm = ChatOllama(model="llama3.2", temperature=0.7)

# ==================== STATE DEFINITION ====================
class State(TypedDict):
    messages: Annotated[list, add_messages]
    master_profile: dict       # Holds ALL data (AI + Frontend)
    focused_profile: dict      # Holds ONLY relevant data (Filtered)
    job_posting: str
    analysis: dict
    resume: str
    cover_letter: str
    screening_answers: str

# ==================== 1. PROFILE DATABASE ====================
def profile_collector(state: State) -> State:
    # Only load profile if not already loaded
    if state.get("master_profile"):
        return {}
    
    # WE SPLIT SKILLS & EXP INTO CATEGORIES HERE
    master_profile = {
        "name": "Your Name",
        "education": "BSc Electrical & Computer Engineering, Addis Ababa University (CGPA 3.8)",
        "contact": "addis.dev@example.com | +251-911-000000",
        
        "data": {
            "ai": {
                "skills": ["Python", "PyTorch", "TensorFlow", "OpenCV", "NLP", "HuggingFace", "RAG", "Pandas"],
                "experience": [
                    "AI Researcher: Developed Amharic Speech-to-Text model using Transformers.",
                    "Computer Vision Intern: Built crop disease detection system for Ethiopian Coffee."
                ],
                "projects": ["Sentiment Analysis on Telegram Data", "Traffic Sign Detection"]
            },
            "frontend": {
                "skills": ["React.js", "Next.js", "TypeScript", "Tailwind CSS", "Figma", "Redux", "HTML5/CSS3"],
                "experience": [
                    "Frontend Developer: Built e-commerce dashboard for local startup using Next.js.",
                    "UI/UX Designer: Designed and implemented responsive landing pages."
                ],
                "projects": ["Personal Portfolio Website", "Real-time Chat App UI"]
            }
        }
    }
    return {"master_profile": master_profile}

# ==================== 2. SMART JOB ANALYZER (The Logic Fix) ====================
def job_analyzer(state: State) -> State:
    # 1. Combine Job Post + User Message to understand intent
    job_text = state.get("job_posting", "")
    user_msg = state["messages"][-1].content
    full_context = (job_text + " " + user_msg).lower()
    
    # 2. Keyword Detection
    ai_keywords = ["ai", "machine learning", "deep learning", "python", "data scientist", "nlp", "vision", "llama", "gpt"]
    frontend_keywords = ["frontend", "react", "javascript", "typescript", "web developer", "css", "ui", "ux", "html"]
    
    is_ai = any(k in full_context for k in ai_keywords)
    is_frontend = any(k in full_context for k in frontend_keywords)
    
    master = state["master_profile"]
    target_role = "Software Engineer"
    
    # 3. HARD FILTERING (Python Logic)
    # We construct a specific list. The LLM never sees the excluded data.
    
    final_skills = []
    final_exp = []
    
    if is_ai and not is_frontend:
        # AI ONLY
        print("--- DETECTED: AI MODE ---")
        target_role = "AI Engineer"
        final_skills = master["data"]["ai"]["skills"]
        final_exp = master["data"]["ai"]["experience"]
        
    elif is_frontend and not is_ai:
        # FRONTEND ONLY
        print("--- DETECTED: FRONTEND MODE ---")
        target_role = "Frontend Developer"
        final_skills = master["data"]["frontend"]["skills"]
        final_exp = master["data"]["frontend"]["experience"]
        
    else:
        # HYBRID / GENERAL
        print("--- DETECTED: GENERAL MODE ---")
        target_role = "Full Stack AI Developer"
        # Combine both lists
        final_skills = master["data"]["ai"]["skills"] + master["data"]["frontend"]["skills"]
        final_exp = master["data"]["ai"]["experience"] + master["data"]["frontend"]["experience"]

    # 4. Create the Focused Profile
    focused_profile = {
        "name": master["name"],
        "education": master["education"],
        "contact": master["contact"],
        "relevant_skills": final_skills,       # ONLY includes selected domain
        "relevant_experience": final_exp       # ONLY includes selected domain
    }
    
    return {
        "focused_profile": focused_profile,
        "analysis": {"role": target_role}
    }

# ==================== 3. ROUTING ====================
def route_request(state: State):
    text = state["messages"][-1].content.lower()
    if any(w in text for w in ["resume", "cv"]): return "resume_generator"
    if "cover" in text: return "cover_letter_generator"
    if any(w in text for w in ["screen", "question", "answer", "interview"]): return "screening_generator"
    return "resume_generator"

# ==================== 4. GENERATORS ====================
def resume_generator(state: State) -> State:
    # We use 'focused_profile' here, so the LLM literally cannot include wrong info
    prompt = ChatPromptTemplate.from_template(
        "Write a resume for a {role}.\n"
        "STRICTLY use only this data provided:\n{profile}\n"
        "Job Description: {job_posting}\n"
        "Format: Markdown."
    )
    resume = (prompt | llm).invoke({
        "profile": state["focused_profile"],
        "role": state["analysis"]["role"],
        "job_posting": state.get("job_posting", "")
    }).content
    return {"resume": resume}

def cover_letter_generator(state: State) -> State:
    prompt = ChatPromptTemplate.from_template(
        "Write a cover letter for a {role}.\n"
        "Highlight these specific experiences only:\n{profile}\n"
        "Job Description: {job_posting}\n"
    )
    cover = (prompt | llm).invoke({
        "profile": state["focused_profile"],
        "role": state["analysis"]["role"],
        "job_posting": state.get("job_posting", "")
    }).content
    return {"cover_letter": cover}

def screening_generator(state: State) -> State:
    prompt = ChatPromptTemplate.from_template(
        "Act as an interviewer for a {role} position.\n"
        "Based on my specific skills: {profile}\n"
        "Ask 3 technical questions and provide the ideal answers based on my experience."
    )
    answers = (prompt | llm).invoke({
        "profile": state["focused_profile"],
        "role": state["analysis"]["role"]
    }).content
    return {"screening_answers": answers}

# ==================== GRAPH SETUP ====================
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
compiled_graph = graph.compile(checkpointer=memory)

# ==================== UI ====================
def chat_with_agent(message: str, history: list, job_description: str = ""):
    inputs = {"messages": [HumanMessage(content=message)]}
    if job_description.strip():
        inputs["job_posting"] = job_description.strip()

    # Config thread_id ensures memory persists across the chat
    config = {"configurable": {"thread_id": "session_1"}}
    
    result = compiled_graph.invoke(inputs, config=config)

    # Helper to format output with the detected role title
    role_title = result['analysis']['role']
    
    if result.get("cover_letter"):
        resp = f"### ✉️ Cover Letter ({role_title})\n\n{result['cover_letter']}"
    elif result.get("resume"):
        resp = f"### 📄 Resume ({role_title})\n\n{result['resume']}"
    elif result.get("screening_answers"):
        resp = f"### 🎤 Interview Prep ({role_title})\n\n{result['screening_answers']}"
    else:
        resp = result["messages"][-1].content

    history = history or []
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": resp})
    return "", history

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🧠 Smart Job Agent: Context Aware")
    gr.Markdown("Try typing: **'Write a resume for a React Developer'** (It will hide AI skills) or **'Resume for AI'** (It will hide Frontend skills).")

    with gr.Row():
        with gr.Column(scale=1):
            job_box = gr.Textbox(label="Job Description (Optional)", lines=10, placeholder="Paste text here...")
        with gr.Column(scale=2):
            chatbot = gr.Chatbot(height=500, type="messages")
            msg = gr.Textbox(label="Request", placeholder="e.g., Generate resume...")
            btn = gr.Button("Submit", variant="primary")

    btn.click(chat_with_agent, [msg, chatbot, job_box], [msg, chatbot])
    msg.submit(chat_with_agent, [msg, chatbot, job_box], [msg, chatbot])

demo.launch()