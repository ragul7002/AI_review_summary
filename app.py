import os
import gradio as gr
from langchain_groq import ChatGroq


# ====================================
# LOAD API KEY FROM ENVIRONMENT
# ====================================

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("❌ GROQ_API_KEY not found. Set it using: setx GROQ_API_KEY 'your_key'")

# ====================================
# INITIALIZE MODEL
# ====================================

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.4,
    groq_api_key=api_key   # ✅ Secure method
)

# ====================================
# FUNCTIONS
# ====================================

def search_papers(topic, num_papers):
    if not topic:
        return "Please enter a topic first."

    papers = [f"{i+1}. {topic} Research Study {i+1}" for i in range(num_papers)]
    return "\n".join(papers)


def generate_draft(topic):
    if not topic:
        return "Please enter a research topic."

    prompt = f"""
    Generate a structured academic research review on the topic: {topic}

    Include:
    - ABSTRACT (100 words)
    - INTRODUCTION
    - METHODS COMPARISON
    - RESULTS SYNTHESIS
    - CONCLUSION
    - FUTURE WORK

    Use formal academic style.
    """

    response = llm.invoke(prompt)
    return response.content


def evaluate_quality(draft):
    if not draft:
        return "Generate draft first."

    prompt = f"""
    Evaluate this research draft:

    {draft}

    Provide:
    - Quality Score (0-10)
    - Strengths
    - Weaknesses
    - Suggestions
    """

    response = llm.invoke(prompt)
    return response.content


def export_txt(draft):
    if not draft:
        return None

    file_path = "research_review.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(draft)

    return file_path


# ====================================
# STYLISH UI
# ====================================

custom_css = """
body {
    background: linear-gradient(135deg, #1f1c2c, #928dab);
}

button {
    border-radius: 12px !important;
    transition: 0.3s;
}

button:hover {
    transform: scale(1.05);
}
"""

with gr.Blocks(css=custom_css, theme=gr.themes.Glass()) as demo:

    gr.Markdown(
        """
        <h1 style='text-align:center; color:white;'>
        📚 AI Research Paper Review System
        </h1>
        <h3 style='text-align:center; color:white;'>
        ✨ Smart Academic Draft Generator
        </h3>
        """
    )

    topic_input = gr.Textbox(
        label="Enter Research Topic",
        placeholder="Eg: Artificial Intelligence in Healthcare"
    )

    with gr.Tabs():

        with gr.Tab("🔎 Research"):
            num_papers = gr.Slider(1, 5, value=3, label="Number of Papers")
            search_btn = gr.Button("🚀 Search Papers")
            papers_output = gr.Textbox(lines=6)

            search_btn.click(
                fn=search_papers,
                inputs=[topic_input, num_papers],
                outputs=papers_output
            )

        with gr.Tab("✍ Generate Draft"):
            generate_btn = gr.Button("✨ Generate Draft")
            draft_output = gr.Textbox(lines=20)

            generate_btn.click(
                fn=generate_draft,
                inputs=topic_input,
                outputs=draft_output
            )

        with gr.Tab("🧠 AI Review"):
            review_btn = gr.Button("🔍 Evaluate Quality")
            review_output = gr.Textbox(lines=10)

            review_btn.click(
                fn=evaluate_quality,
                inputs=draft_output,
                outputs=review_output
            )

        with gr.Tab("⬇ Export"):
            download_file = gr.File()

            draft_output.change(
                fn=export_txt,
                inputs=draft_output,
                outputs=download_file
            )

demo.launch(server_port=7860)
