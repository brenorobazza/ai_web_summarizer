from Scraper import Scraper
from Brave import Brave
from Agent import Agent

import json
import sys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
def main(search_query, provider, n=4):
    
    brave = Brave()
    results = brave.get_search_results(search_query)
    scraper = Scraper()
    # Print the results
    print(f"Search results for '{search_query}':")
    all_content = []
    for result in results[:n]: # get n results
        print(f"\n> Getting content from {bcolors.WARNING}{result['url']}{bcolors.ENDC}\n> Title: {result['title']}")
        content = json.loads(scraper.scrape_page(result['url'], "json", 1))
        all_content.append(result['title'])
        all_content.extend(content["paragraphs"])
    
    # Summarize the content
    print("\n> Summarizing content...")
    
    instructions = """
    You are an expert news summarizer tasked with analyzing the content of search results and producing a detailed and context-rich summary.
    Your summary must:

    - Clearly explain the main event or topic, including what happened, where and when
    - Identify the key people, organizations or countries involved
    - Describe any relevant background context that helps the reader understand why this event matters
    - Include any reactions, implications, or potential consequences
    - Be written in a clear, neutral tone, avoiding opinion or exaggeration
    - Be self-contained, it should make sense without needing to read the original articles

    Use 1-3 concise paragraphs, depending on the complexity of the topic.
    The content of the search results is below:
    """
    summarizer = Agent(provider, instructions=instructions)
    summary = summarizer.invoke(prompt="\n".join(all_content))
    return summary
    
if __name__ == "__main__":
    # Accept -p <provider> and the rest as search query
    if len(sys.argv) < 4 or sys.argv[1] != "-p":
        print("Usage: python news_summarizer.py -p <provider> <search_query>")
        sys.exit(1)

    provider = sys.argv[2]
    search_query = " ".join(sys.argv[3:])
    if not search_query.strip():
        print("Error: No search query provided.")
        print("Usage: python news_summarizer.py -p <provider> <search_query>")
        sys.exit(1)

    result = main(search_query, provider, n=4)
    print(result)