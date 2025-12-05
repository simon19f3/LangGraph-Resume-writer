import gradio as gr
from langchain_core.messages import HumanMessage
from graph import build_graph

compiled_graph = build_graph()

def chat_with_agent(message, history, job_description=""):
    inputs = {"messages": [HumanMessage(content=message)]}

    if job_description.strip():
        inputs["job_posting"] = job_description

    config = {"configurable": {"thread_id": "session_1"}}
    result = compiled_graph.invoke(inputs, config=config)

    role = result["analysis"]["role"]

    if result.get("resume"):
        resp = f"### 📄 Resume ({role})\n\n{result['resume']}"
    elif result.get("cover_letter"):
        resp = f"### ✉️ Cover Letter ({role})\n\n{result['cover_letter']}"
    else:
        resp = f"### 🎤 Interview Prep ({role})\n\n{result['screening_answers']}"

    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": resp})
    return "", history


with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🧠 Smart Job Agent (LangGraph + Ollama)")

    with gr.Row():
        job_box = gr.Textbox(label="Job Description", lines=8)
        chatbot = gr.Chatbot(height=500, type="messages")
    
    msg = gr.Textbox(label="Your Request")
    btn = gr.Button("Send")

    btn.click(chat_with_agent, [msg, chatbot, job_box], [msg, chatbot])
    msg.submit(chat_with_agent, [msg, chatbot, job_box], [msg, chatbot])

demo.launch()
