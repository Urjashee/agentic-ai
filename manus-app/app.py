import gradio as gr
from sidekick import Sidekick
import os
import asyncio


async def process_message(sidekick, message, success_criteria, history):
    if sidekick is None:
        return history + [{"role": "assistant", "content": "⚠️ Please initialize Sidekick first."}], sidekick
    results = await sidekick.run_superstep(message, success_criteria, history)
    return results, sidekick


async def reset(api_key):
    if not api_key or not api_key.startswith("sk-"):
        return "", "", None, None, "⚠️ Enter a valid API key before resetting."
    new_sidekick = Sidekick(api_key=api_key)
    await new_sidekick.setup()
    return "", "", None, new_sidekick, "✅ API Key reset successfully!"


def free_resources(sidekick):
    print("Cleaning up")
    try:
        if sidekick:
            sidekick.cleanup()
    except Exception as e:
        print(f"Exception during cleanup: {e}")


async def init_sidekick(api_key):
    if not api_key or not api_key.startswith("sk-"):
        return None, "❌ Please enter a valid API key (sk-...)"
    sidekick = Sidekick(api_key=api_key)
    await sidekick.setup()
    return sidekick, "✅ API Key initialized!"


with gr.Blocks(title="Sidekick", theme=gr.themes.Default(primary_hue="emerald")) as ui:
    gr.Markdown("## 🔑 Enter your OpenAI API Key")
    api_key = gr.Textbox(
        label="OPENAI_API_KEY",
        type="password",
        placeholder="sk-...",
    )

    sidekick = gr.State(delete_callback=free_resources)

    status = gr.Markdown("Waiting for API key...")

    init_button = gr.Button("Initialize API Key", variant="primary")

    gr.Markdown("## 🤖 Sidekick Personal Co-Worker")

    with gr.Row():
        chatbot = gr.Chatbot(label="Sidekick", height=300, type="messages")

    with gr.Group():
        with gr.Row():
            message = gr.Textbox(show_label=False, placeholder="Your request to the Sidekick")
        with gr.Row():
            success_criteria = gr.Textbox(
                show_label=False, placeholder="What are your success criteria?"
            )

    with gr.Row():
        reset_button = gr.Button("Reset", variant="stop")
        go_button = gr.Button("Go!", variant="primary")

    # Button wiring
    init_button.click(init_sidekick, [api_key], [sidekick, status])

    message.submit(process_message, [sidekick, message, success_criteria, chatbot], [chatbot, sidekick])
    success_criteria.submit(process_message, [sidekick, message, success_criteria, chatbot], [chatbot, sidekick])
    go_button.click(process_message, [sidekick, message, success_criteria, chatbot], [chatbot, sidekick])
    reset_button.click(reset, [api_key], [message, success_criteria, chatbot, sidekick, status])


ui.launch(inbrowser=True)
