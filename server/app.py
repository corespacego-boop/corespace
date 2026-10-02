import os
import uvicorn
from main import app

# Mount a lightweight Gradio interface at /gradio so Hugging Face Space
# fully recognizes the Gradio SDK while serving our corespace HTML dashboard at /
try:
    import gradio as gr

    with gr.Blocks(title="corespace API") as demo:
        gr.Markdown(
            """
            # 🚀 corespace API Server
            Academic data scraper and backend API for SRM students.
            
            - **Web Dashboard**: [Click here to open Dashboard](/)
            - **Interactive Swagger Docs**: [Click here to view /docs](/docs)
            - **Version Endpoint**: [/version](/version)
            """
        )
    app = gr.mount_gradio_app(app, demo, path="/gradio")
except Exception as e:
    print(f"[corespace] Gradio mount optional: {e}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=False)
