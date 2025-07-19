from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

import bs4 as bs
import sys
import time
import json
import os
from urllib.parse import urlparse


# Scraper class encapsulating driver and scraping logic
class Scraper:
    def __init__(self):
        self.options = Options()
        show_browser = os.environ.get("SHOW_BROWSER", "0")
        if show_browser not in ("1", "true", "True"):  # Default: headless
            self.options.add_argument("--headless")
            self.options.add_argument("--disable-gpu")
        self.options.add_argument("--log-level=3")  # Suppress ChromeDriver logs
        self.service = Service(log_path=os.devnull)
        self.driver = webdriver.Chrome(options=self.options, service=self.service)

    def scrape_page(self, url, output_format="text", wait_time=0):
        try:
            self.driver.get(url)
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            if wait_time > 0:
                time.sleep(wait_time)
            soup = bs.BeautifulSoup(self.driver.page_source, 'html.parser')
            title = soup.title.string.strip() if soup.title and soup.title.string else ""
            meta_desc = ""
            meta_tag = soup.find('meta', attrs={'name': 'description'})
            if meta_tag and meta_tag.get('content'):
                meta_desc = meta_tag['content'].strip()
            canonical = ""
            link_tag = soup.find('link', rel='canonical')
            if link_tag and link_tag.get('href'):
                canonical = link_tag['href']
            paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]
            headings = {tag: [h.get_text(strip=True) for h in soup.find_all(tag)] for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']}
            links = [a['href'] for a in soup.find_all('a', href=True)]
            lists = [li.get_text(strip=True) for li in soup.find_all('li')]
            tables = []
            for table in soup.find_all('table'):
                rows = []
                for tr in table.find_all('tr'):
                    cells = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
                    if cells:
                        rows.append(cells)
                if rows:
                    tables.append(rows)
            images = [img.get('alt', '').strip() for img in soup.find_all('img') if img.get('alt')]
            if output_format == "json":
                return json.dumps({
                    "title": title,
                    "meta_description": meta_desc,
                    "canonical_url": canonical,
                    "paragraphs": paragraphs,
                    "headings": headings,
                    "links": links,
                    "lists": lists,
                    "tables": tables,
                    "images_alt": images
                }, ensure_ascii=False, indent=2)
            else:
                parts = []
                if title:
                    parts.append(f"Title: {title}")
                if meta_desc:
                    parts.append(f"Meta Description: {meta_desc}")
                if canonical:
                    parts.append(f"Canonical URL: {canonical}")
                if paragraphs:
                    parts.append("\nParagraphs:")
                    parts.extend(paragraphs)
                if any(headings.values()):
                    parts.append("\nHeadings:")
                    for tag, items in headings.items():
                        if items:
                            parts.append(f"{tag}: " + ", ".join(items))
                if lists:
                    parts.append("\nLists:")
                    parts.extend(lists)
                if tables:
                    parts.append("\nTables:")
                    for table in tables:
                        for row in table:
                            parts.append(" | ".join(row))
                if images:
                    parts.append("\nImage Alt Texts:")
                    parts.extend(images)
                if links:
                    parts.append("\nLinks:")
                    parts.extend(links)
                return parts
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return None

    def close(self):
        self.driver.quit()


def get_domain_name(url):
    """
    Extracts and returns the domain name of an url
    """
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    # Remove 'www.' prefix if present
    if domain.startswith("www."):
        domain = domain[4:]

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
    output_format = "text"
    wait_time = 0
    if len(sys.argv) > 2:
        if sys.argv[2].lower() == "json":
            output_format = "json"
        else:
            try:
                wait_time = int(sys.argv[2])
            except ValueError:
                pass
    if len(sys.argv) > 3:
        try:
            wait_time = int(sys.argv[3])
        except ValueError:
            pass
    print(f"Scraping data from {url} (format: {output_format}, wait: {wait_time}s)...")
    scraper = Scraper()
    scraped_data = scraper.scrape_page(url, output_format, wait_time)
    print("Scraped content:")
    if output_format == "json":
        print(scraped_data)
    else:
        for item in scraped_data:
            print(item)
    scraper.close()
