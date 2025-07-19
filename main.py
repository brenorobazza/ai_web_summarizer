from Scraper import Scraper
from Brave import Brave
from Summarizer import Summarizer

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
    summarizer = Summarizer(provider)
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
    You are an expert news summarizer that examines the content of search results and provides a concise summary.
    Your summary should highlight the key aspects of the content, including main events, people involved, and any significant outcomes.
    This is the content of the search results:
    """
    summary = summarizer.summarize_text("\n".join(all_content), instructions=instructions)
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