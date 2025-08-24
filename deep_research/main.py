import gradio as gr
from dotenv import load_dotenv
from research_manager import ResearchManager
import openai

load_dotenv(override=True)


async def run(query: str, api_key: str):
    try:
        async for chunk in ResearchManager().run(query, api_key):
            yield chunk
    except openai.AuthenticationError as e:
        # Show clean error message
        yield f"❌ Authentication failed:\n\n{e}"
    except Exception as e:
        # Show any other error
        yield f"⚠️ Error: {str(e)}"


with gr.Blocks(theme=gr.themes.Default(primary_hue="sky")) as ui:
    gr.Markdown("# Deep Research")
    api_key_text_box = gr.Textbox(label="Please enter your OPENAI_API_KEY here")
    query_textbox = gr.Textbox(label="What topic would you like to research?")
    run_button = gr.Button("Run", variant="primary")
    report = gr.Markdown(label="Report")

    run_button.click(fn=run, inputs=[query_textbox, api_key_text_box], outputs=report)
    query_textbox.submit(fn=run, inputs=[query_textbox, api_key_text_box], outputs=report)

ui.launch(inbrowser=True)

