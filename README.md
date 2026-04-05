# AI Research Copilot 

An autonomous AI agent built with **Python**, **Ollama**, and **Llama 3.2**. This agent can browse the web, summarize content, and decide when it needs to use external tools.

## Features
- **Autonomous Tool Use:** Uses ReAct logic to decide if a URL needs to be fetched.
- **Local Inference:** Runs entirely on your machine using Ollama (Privacy-focused).
- **Web Scraping:** Built-in capability to clean and parse HTML for LLM context.
##  System Architecture

## The agent follows a **Reason-Act (ReAct)** pattern:
1. **Input:** Receives user query (e.g., "Summarize this article: [URL]").
2. **Reasoning:** The LLM determines if it has the necessary information or needs a tool.
3. **Action:** If a URL is present, the agent invokes the `web_search` function.
4. **Observation:** The Python script scrapes the HTML, cleans it, and feeds it back to the LLM.
5. **Output:** The LLM generates a final response based on the retrieved data.
## Tech Stack
- **LLM:** Llama 3.2 (via Ollama)
- **Language:** Python 3.10+
- **Libraries:** Requests, BeautifulSoup4, Ollama-python

## How to Run
1. Install [Ollama](https://ollama.com/)
2. `ollama run llama3.2`
3. `pip install -r requirements.txt`
4. `python3 copilot.py`

