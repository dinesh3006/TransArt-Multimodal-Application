# TransArt: An All-in-One AI Suite 🤖

TransArt is a powerful, web-based multimodal application that seamlessly integrates language processing, image synthesis, and conversational AI.This project demonstrates a complete workflow from translating vernacular languages (like Tamil) to English, and then using that output to generate stunning visuals and engage in intelligent conversation.

***

## ✨ Live Demo

**(Add the link to your live Hugging Face Spaces app here)**

`Running on public URL: https://06d61591268078069d.gradio.live`

***

## 🚀 Core Features

This application is built with a user-friendly tabbed interface in Gradio, offering three distinct AI-powered tools:

**🎙️ Audio to Text & Image**: Transcribe **Tamil** or **English** audio using `whisper-large-v3`, translate it to English with an LLM, and generate an image from the text using `Stable Diffusion XL`.
**🖼️ Prompt to Image**: Enter any descriptive text prompt and generate a high-quality image, perfect for content creators and designers.
**💬 AI Chatbot**: Engage in an intelligent conversation with a helpful AI assistant powered by Groq's fast inference engine.

***

## 🛠️ Tech Stack & Models

This project leverages a modern stack of AI technologies and APIs to deliver high performance:

**Framework**: **Gradio** for the interactive web UI.
**AI Inference**:
    **[Groq API](https://groq.com/)**: For ultra-fast audio transcription and LLM responses.
    **[Hugging Face Inference API](https://huggingface.co/inference-api)**: For robust and reliable text-to-image generation.
**Models**:
    **Audio Transcription**: `whisper-large-v3`
    **Translation & Chat**: `moonshotai/kimi-k2-instruct`
    **Image Generation**: `stabilityai/stable-diffusion-xl-base-1.0`

***

## ☁️ Deployment to Hugging Face Spaces

This application is designed to be deployed directly to Hugging Face Spaces. [cite: 10, 47] Here’s the step-by-step guide.

### 1. Prepare Your Files
Make sure you have the following two files ready:

* **`app.py`**: The main Python script with your Gradio application code.
* **`requirements.txt`**: A text file listing the project's dependencies. It must contain:
    ```
    gradio
    groq
    huggingface_hub
    ```

### 2. Create a New Space
* Go to [Hugging Face](https://huggingface.co/) and click on **"New Space"**.
* Give your Space a name (e.g., "TransArt-AI-Suite").
* Select **"Gradio"** as the SDK.
* Click **"Create Space"**.

### 3. Upload Your Files
* In your new Space, navigate to the **"Files"** tab.
* Click on **"Add file"** and select **"Upload file"**.
* Upload your `app.py` and `requirements.txt` files.
* Commit the files directly to the `main` branch.

### 4. Add Your API Keys as Secrets
This is the most important step for security. **Never paste your keys directly into your code.**

* In your Space, go to the **"Settings"** tab.
* Find the **"Repository secrets"** section on the left.
* Click **"New secret"** and add your Groq API key:
    * **Name**: `GROQ_API_KEY`
    * **Secret value**: `gsk_YourGroqApiKeyGoesHere`
* Click **"New secret"** again to add your Hugging Face Token:
    * **Name**: `HUGGING_FACE_API_KEY`
    * **Secret value**: `hf_YourHuggingFaceTokenGoesHere`

The application will automatically build and launch. Your AI Suite will be live within a few moments!

***

## 📸 Application Screenshots

**(Action Required: Replace the placeholders below with actual screenshots of my running application.)**

**Tab 1: Audio Processing in action**
<img width="1920" height="911" alt="Screenshot 2025-10-17 172253" src="https://github.com/user-attachments/assets/b1cd642c-e4b8-4d31-8648-49b3ff0ca1e8" />
<br/>
<img width="1920" height="914" alt="Screenshot 2025-10-17 172449" src="https://github.com/user-attachments/assets/0bb2b95b-bf52-493d-bda0-2a4d00d8bf4a" />

``

**Tab 2: Image generation from a text prompt**
<img width="1920" height="908" alt="Screenshot 2025-10-17 172813" src="https://github.com/user-attachments/assets/e3910d95-6bd5-4c92-86ec-64e0b707f840" />

``

**Tab 3: Engaging with the AI Chatbot**
<img width="1920" height="903" alt="Screenshot 2025-10-17 174926" src="https://github.com/user-attachments/assets/e65aa001-9e07-4bcd-b1fb-6a73194c67b8" />


``

***

## 📜 License

This project is licensed under the MIT License.
