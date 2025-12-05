from state.state_types import State

def profile_collector(state: State) -> State:
    if state.get("master_profile"):
        return {}

    master_profile = {
        "name": "Your Name",
        "education": "BSc Electrical & Computer Engineering, Addis Ababa University (CGPA 3.8)",
        "contact": "addis.dev@example.com | +251-911-000000",

        "data": {
            "ai": {
                "skills": [
                    "Python", "PyTorch", "TensorFlow", "OpenCV", "NLP",
                    "HuggingFace", "RAG", "Pandas"
                ],
                "experience": [
                    "AI Researcher: Developed Amharic Speech-to-Text model using Transformers.",
                    "Computer Vision Intern: Built coffee crop disease detection system."
                ],
            },

            "frontend": {
                "skills": [
                    "React.js", "Next.js", "TypeScript", "Tailwind CSS",
                    "Figma", "Redux"
                ],
                "experience": [
                    "Frontend Developer: Built e-commerce dashboard using Next.js.",
                    "UI/UX Designer: Designed responsive landing pages."
                ],
            }
        }
    }

    return {"master_profile": master_profile}
