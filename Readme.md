A smart, stateful chatbot that writes perfectly tailored resumes and cover letters for you — and never forgets who you are.
You tell it about yourself once (your experience, skills, projects, education…).
Paste any job description.
Ask for a “resume”, or “cover letter”.
In seconds you get ATS-friendly documents that actually match the job.
Close the app, come back days or weeks later — it still remembers everything about you. No need to repeat yourself ever again.
Built from the ground up with LangGraph (the same framework companies like Klarna, Replit, and Uber use for production agents), this isn’t just another prompt wrapper — it’s a real multi-step, stateful agent with memory, branching logic, and persistence.

# Features


Persistent shared state across sessions
Clear nodes for each responsibility (collect profile → analyze job → generate documents)
Conditional routing (resume vs cover letter vs both)
Human-in-the-loop conversation for gathering your info
Real checkpointer memory (MemorySaver) so nothing gets lost
Easy to extend with loops (e.g., “make it better” → regenerate)

Professors and recruiters instantly recognize this as “someone who actually understands agents,” not just copy-pasting from a tutorial.
# How It Works (the flow)

First chat → The agent asks friendly questions to build your full professional profile (you can paste your old resume too).
Whenever you apply somewhere → Paste the job description and say what you need.
The graph runs:
Profile Collector (only on first run) → Job Analyzer → (conditional branch) → Resume Generator and/or Cover Letter Generator
You get beautifully tailored output, ready to download or copy.

Because everything is saved with a thread ID, every future conversation picks up exactly where you left off.
Quick Local Setup

git clone https://github.com/simon19f3/LangGraph-Resume-writer.git

`cd LangGraph-Resume-writer`

`pip install -r requirements.txt`

# Set your LLM API key (OpenAI, Anthropic, Grok, etc.)
export OPENAI_API_KEY=sk-...

streamlit run app.py
Open your browser to http://localhost:8501 and start chatting!
Tech Highlights

LangGraph + LangChain (stateful graphs, tools, memory)
Streamlit for the simple chat UI
MemorySaver checkpointer (persists your profile forever)
Works with any LLM (just change the model name)

Ideas for Extending It (if you want to level up)

Add a “critique & regenerate” loop when you say “make it stronger”
Export directly to PDF or DOCX
Multiple saved profiles (switch between “software engineer me” and “product manager me”)
Host it publicly with user accounts
Add LinkedIn profile import
