# Web Scraper & News Summarizer

## Overview

This project is a Python-based web scraping and summarization tool. It automates the process of searching for news articles or other types of webpages, scraping their content, and generating concise summaries using either OpenAI or Ollama (Llama3.2 - Local) language models. The tool is modular, allowing for easy extension and customization.


## Features
- **Automated Web Search:** Uses the Brave Search API to find relevant website pages based on a user query.
- **Web Scraping:** Extracts content (titles, paragraphs, headings, links, etc.) from the resulting web pages using Selenium and BeautifulSoup.
- **Summarization:** Summarizes the scraped content using either OpenAI or Ollama (Llama3.2) models, depending on your configuration, via the `Agent` class.


## File Structure
- `main.py` — Main entry point for running the summarizer.
- `Brave.py` — Handles Brave Search API integration.
- `Scraper.py` — Contains the web scraping logic.
- `Agent.py` — Summarizes text using OpenAI or Ollama (replaces the previous Summarizer class).
- `requirements.txt` — Python dependencies.
- `.env` — Store your API keys and environment variables here (see below).

## Setup Instructions

1. **Clone the repository and install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

2. **Configure API Keys:**
   - Create a `.env` file in the project root (if not present).
   - Add your API keys as follows:
     ```env
     BRAVE_API_KEY="your_brave_api_key_here"
     OPENAI_API_KEY="your_openai_api_key_here"
     ```
   - These keys are required for the Brave Search API and OpenAI summarization provider. The program loads them automatically from the `.env` file.

3. **Run the Summarizer:**
   ```sh
   python main.py -p <provider> <search_query>
   ```
   - `<provider>`: Either `openai` or `ollama` (for Llama3.2 via Ollama).
   - `<search_query>`: The news topic or keywords to search for.

   **Example:**
   ```sh
   python main.py -p openai "Liquid Glass release by Apple"
   ```

## Notes
- The `.env` file is included in `.gitignore` and should **not** be committed to version control.
- You can switch between OpenAI and Ollama summarization by changing the provider argument.
- The summarizer will print a concise summary of the top search results for your query.
- The summarization logic is now handled by the `Agent` class in `Agent.py`.
