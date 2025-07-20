import streamlit as st
from Brave import Brave
from Agent import Agent
from Scraper import Scraper
import json

def determine_search_terms(provider, prompt):
    instructions = """
    You are an expert in formulating highly effective web search queries.
    Your task is to receive a question or topic and generate one optimized search query that retrieves the most relevant and up-to-date information, based on the underlying intent behind the input.
    You must:
    - Interpret what the user is really trying to find out, not just rewrite their words
    - Focus the query on the most relevant keywords and context (e.g. if the topic is a company, consider recent activity like product releases, leadership changes, partnerships, etc.)
    - Include time context only when it helps narrow down results (e.g. “this week”). DO NOT add any date unless it is already in the prompt
    - Keep the query compact and keyword-rich, without conversational or filler words
    - Output exactly one search query, nothing else
    - Answer in the same language that the prompt is given

    Example:
    - Input: What is the latest news about Apple?
    - Output: Apple recent product launches and announcements
    """
    
    searcher_agent = Agent(provider, instructions)
    terms = searcher_agent.invoke(prompt)
    print(terms)
    # remove symbols from terms
    terms = terms.replace("?", "").replace("!", "").replace(".", "").replace(",", "")
    return terms

def summarize(provider, content:str):
    instructions = """
    You are an expert news summarizer tasked with analyzing the content of search results and producing a detailed and context-rich summary.
    Your summary must:

    - Clearly explain the main event or topic, including what happened, where and when
    - Identify the key people, organizations or countries involved
    - Describe any relevant background context that helps the reader understand why this event matters
    - Include any reactions, implications, or potential consequences
    - Be written in a clear, neutral tone, avoiding opinion or exaggeration
    - Be self-contained, it should make sense without needing to read the original articles
    - Use markdown formatting for readability, including headings and bullet points where appropriate

    Use 1-3 concise paragraphs, depending on the complexity of the topic.
    The content of the search results is below:
    """
    summarizer = Agent(provider=provider, instructions=instructions)
    summary = summarizer.invoke(content)
    return summary
    
st.set_page_config(page_title="Web Content Summarizer", page_icon="📰")
st.title("Web Content Summarizer")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "provider" not in st.session_state:
    st.session_state.provider = "ollama"

# Sidebar
with st.sidebar:
    st.header("Settings")
    provider = st.selectbox("Choose LLM Provider", ["ollama", "openai"], index=0)
    st.session_state.provider = provider

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask for a news summary (e.g. 'Apple AI news')"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Search webpages
    with st.chat_message("assistant"):
        with st.status("Searching the web..."):
            brave = Brave()
            scraper = Scraper()
            
            results = []
            
            while len(results) == 0:
                search_term = determine_search_terms(st.session_state.provider, prompt)
                st.write(search_term)
                results = brave.get_search_results(search_term)

            st.write(f"Reading results")
            
            all_content = []
            for result in results[:4]: # get 4 results
                st.write(f"> Reading '{result['title']}' from '{result['url']}'")
                content = json.loads(scraper.scrape_page(result['url'], "json", 1))
                all_content.append(result['title'])
                all_content.extend(content["paragraphs"])
            st.write("Reading finished")
    
    # Summarize
    with st.chat_message("assistant"):
        with st.status("Summarizing"):
            try:
                response = summarize(st.session_state.provider, ";".join(all_content))
            except Exception as e:
                response = f"Error: {e}"
        st.markdown(response)
                
    st.session_state.messages.append({"role": "assistant", "content": response})