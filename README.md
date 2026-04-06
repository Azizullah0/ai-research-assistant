# Multimodal AI Research Copilot

An autonomous, privacy-first AI agent built with **Python**, **Ollama**, and **Llama 3.2**. This agent is designed to be a "Universal Ingestion" engine—it doesn't just chat; it **sees** images, **hears** voice notes, **reads** complex documents (PPTX, PDF, DOCX), and **searches** the live web.

##  Key Features
- **Universal File Support:** Built-in parsing for PDF, PPTX, DOCX, and XLSX using Microsoft's `MarkItDown`.
- **Vision Integration:** High-speed image description using the **Moondream** (1.6B) vision model.
- **Voice-to-Text:** Local speech transcription via **OpenAI Whisper** (No API keys required).
- **Model Orchestration:** A "Specialist/Generalist" pipeline that routes vision tasks to Moondream and reasoning tasks to Llama 3.2.
- **Autonomous Tool Use:** Implements ReAct logic to decide when to invoke web-scraping tools for real-time data.

## System Architecture

The agent follows a **Multi-Stage Inference Pipeline** to maximize performance on consumer-grade hardware (16GB RAM):

1.  **Perception Layer:** - **Voice:** Whisper "Tiny" converts audio bytes to text.
    - **Vision:** Moondream processes image pixels into descriptive natural language.
2.  **Augmentation Layer:** - Text from documents and visual descriptions are injected into the LLM context window.
3.  **Reasoning Layer:** - **Llama 3.2 (3B)** analyzes the consolidated context.
4.  **Action Layer:** - If the query requires external data, the agent triggers a custom `web_search` function to scrape and clean HTML content.



## Tech Stack
- **Interface:** Streamlit (v1.30+ with integrated chat input)
- **Inference Engine:** Ollama
- **Models:** Llama 3.2 (Reasoning) & Moondream (Vision)
- **Audio Processing:** FFmpeg & OpenAI Whisper
- **Document Parsing:** Microsoft MarkItDown

##  Installation & Setup

### 1. Prerequisites (Ubuntu/Debian)
Ensure **FFmpeg** is installed for audio handling:

sudo apt update && sudo apt install ffmpeg
### 2. Pull Local Models
Install Ollama and download the required models:

ollama pull llama3.2
ollama pull moondream
### 3. Install Python Dependencies

pip install -r requirements.txt
### 4. Launch the Application

streamlit run app.py

## Project Structure
app.py: Streamlit UI, session state management, and model routing.

agent_engine.py: Core logic for file conversion, voice transcription, and tool definitions.

reader.py: Utility for cleaning and fetching web content for LLM ingestion.

my_docs/: Secure local directory for uploaded research materials.

## Privacy & Security
This project is 100% local. Your voice, images, and documents never leave your machine. It is designed for researchers and professionals who need AI capabilities without compromising data sovereignty.