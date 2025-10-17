import gradio as gr
import os
from groq import AsyncGroq, Groq
from huggingface_hub import InferenceClient

# ==============================================================================
# API KEY SETUP - Gets from Hugging Face Secrets
# ==============================================================================
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
HF_TOKEN = os.environ.get('HUGGING_FACE_API_KEY')

# Validate API keys
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found! Please add it in Space Settings → Secrets")
if not HF_TOKEN:
    raise ValueError("HUGGING_FACE_API_KEY not found! Please add it in Space Settings → Secrets")

# Initialize API clients
groq_async_client = AsyncGroq(api_key=GROQ_API_KEY)
groq_sync_client = Groq(api_key=GROQ_API_KEY)
inference_client = InferenceClient(token=HF_TOKEN)

IMAGE_MODEL_ID = "stabilityai/stable-diffusion-xl-base-1.0"

# ==============================================================================
# CORE FUNCTIONS
# ==============================================================================

async def process_audio_and_generate(audio_path, source_language, generate_image_checkbox):
    if not audio_path:
        gr.Warning("No audio file provided. Please upload an audio file.")
        return "", "", None

    transcription, english_text, image_output = "", "", None
    detected_language = ""

    # 1. Transcribe audio to text
    try:
        with open(audio_path, "rb") as audio_file:
            if source_language == "Auto-detect":
                transcription_result = groq_sync_client.audio.transcriptions.create(
                    file=(audio_path, audio_file.read()),
                    model="whisper-large-v3",
                    response_format="verbose_json"
                )
                detected_language = transcription_result.language
            else:
                lang_code = "ta" if source_language == "Tamil" else "en"
                transcription_result = groq_sync_client.audio.transcriptions.create(
                    file=(audio_path, audio_file.read()),
                    model="whisper-large-v3",
                    language=lang_code,
                    response_format="json"
                )
                detected_language = source_language
        
        transcription = transcription_result.text
        
    except Exception as e:
        gr.Error(f"Transcription failed! Error: {e}")
        return "Transcription Failed", "", None

    # 2. Translate to English if needed
    try:
        if detected_language.lower() in ["english", "en"]:
            english_text = transcription
        else:
            translation_prompt = f"Translate the following text to English. Provide only the English translation and nothing else. Text: '{transcription}'"
            chat_completion = await groq_async_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful translation assistant."},
                    {"role": "user", "content": translation_prompt}
                ],
                model="moonshotai/kimi-k2-instruct",
            )
            english_text = chat_completion.choices[0].message.content.strip()
        
    except Exception as e:
        gr.Error(f"Translation failed! Error: {e}")
        return transcription, "Translation Failed", None

    # 3. Generate image if checkbox is ticked
    if generate_image_checkbox:
        try:
            image_output = inference_client.text_to_image(english_text, model=IMAGE_MODEL_ID)
        except Exception as e:
            gr.Warning(f"Image generation failed! Error: {e}")

    return transcription, english_text, image_output


def generate_image_from_prompt(prompt):
    if not prompt or not prompt.strip():
        gr.Warning("Prompt is empty. Please enter some text.")
        return None
    try:
        image = inference_client.text_to_image(prompt, model=IMAGE_MODEL_ID)
        return image
    except Exception as e:
        gr.Error(f"Image generation failed! Error: {e}")
        return None


async def chatbot_response(message, history):
    history_groq_format = [{"role": "system", "content": "You are a helpful assistant."}]
    for human, assistant in history:
        history_groq_format.append({"role": "user", "content": human})
        history_groq_format.append({"role": "assistant", "content": assistant})
    history_groq_format.append({"role": "user", "content": message})

    try:
        chat_completion = await groq_async_client.chat.completions.create(
            messages=history_groq_format,
            model="moonshotai/kimi-k2-instruct"
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        gr.Error(f"Chatbot failed! Error: {e}")
        return f"Sorry, I encountered an error: {e}"


# ==============================================================================
# GRADIO INTERFACE
# ==============================================================================

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🤖 All-in-One AI Suite")
    gr.Markdown("**Tab 1**: Audio transcription & translation | **Tab 2**: Image generation | **Tab 3**: Chatbot")

    with gr.Tabs():
        # Tab 1: Audio Processing
        with gr.TabItem("🎙️ Audio to Text & Image"):
            with gr.Row():
                with gr.Column(scale=1):
                    audio_input = gr.Audio(type="filepath", label="Upload Audio File")
                    language_dropdown = gr.Dropdown(
                        choices=["Auto-detect", "Tamil", "English"],
                        value="Auto-detect",
                        label="Source Language"
                    )
                    audio_image_checkbox = gr.Checkbox(label="Generate Image from Translation?", value=True)
                    audio_button = gr.Button("Process Audio", variant="primary")
                with gr.Column(scale=2):
                    transcription_output = gr.Textbox(label="Transcription (Original Language)", interactive=False, lines=3)
                    translation_output = gr.Textbox(label="English Text", interactive=False, lines=3)
                    audio_image_output = gr.Image(label="Generated Image")

        # Tab 2: Prompt to Image
        with gr.TabItem("🖼️ Prompt to Image"):
            with gr.Row():
                with gr.Column(scale=2):
                    image_prompt_input = gr.Textbox(label="Enter your prompt", lines=4, placeholder="e.g., A majestic lion in the savanna at sunset...")
                    image_button = gr.Button("Generate Image", variant="primary")
                with gr.Column(scale=1):
                    image_output = gr.Image(label="Generated Image")

        # Tab 3: Chatbot
        with gr.TabItem("💬 Chatbot"):
            gr.ChatInterface(
                chatbot_response,
                title="AI Chatbot",
                description="Ask me anything!",
                examples=[["Hello!"], ["What is the capital of India?"], ["Explain quantum computing"]],
            )

    # Button click actions
    audio_button.click(
        fn=process_audio_and_generate,
        inputs=[audio_input, language_dropdown, audio_image_checkbox],
        outputs=[transcription_output, translation_output, audio_image_output],
    )

    image_button.click(
        fn=generate_image_from_prompt,
        inputs=image_prompt_input,
        outputs=image_output
    )

if __name__ == "__main__":
    demo.launch()