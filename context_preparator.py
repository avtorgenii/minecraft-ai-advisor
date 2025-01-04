import asyncio

from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from googlesearch import search
import requests
from langchain_text_splitters import RecursiveCharacterTextSplitter
from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.chrome.options import Options
from encoder import load_st
from sklearn.metrics.pairwise import cosine_similarity


class ContextPreparator:
    def __init__(self):
        # Duckduck go web search for images
        self.ddgs = DDGS()

        # Selenium web search options
        self.options = Options()
        self.options.add_argument('--headless')  # Run in headless mode (no browser window)
        self.options.add_argument('--disable-gpu')  # Disable GPU for headless mode
        self.options.add_argument('--no-sandbox')  # Necessary for some systems (Linux-based)
        self.options.add_argument('--mute-audio')  # Mute audio
        self.options.add_argument("--disable-webgl")
        self.driver = webdriver.Chrome(options=self.options)

        # Sentence encoder for extracting context
        self.model = load_st()


    def __del__(self):
        try:
            self.driver.close()
        except ImportError:
            pass


    def _search_web_pages(self, query, max_results):
        """Search for web pages using DuckDuckGo."""
        hrefs = []

        try:
            results = self.ddgs.text(query, max_results=max_results)
            hrefs = [res['href'] for res in results]
        except Exception as e:
            print(e)
            try:
                results = search(query, num_results=max_results)
                hrefs = [res for res in results]
            except Exception as e:
                print(e)
                hrefs = []

        return hrefs

    def _selenium_search(self, href):
        """Use Selenium to extract page content."""
        try:
            self.driver.get(href)
            page_content = self.driver.page_source
        except WebDriverException:
            return None
        return page_content

    def _parse_web_page(self, href, for_craft=False):
        """
        Parse the web page and extract text content.
        If for_craft is True, extract items for crafting.
        """
        html = self._selenium_search(href)

        if html is None:
            return None

        soup = BeautifulSoup(html, 'html.parser')

        return soup.get_text(separator=' ', strip=True)

    def _split_htmls_into_documents(self, htmls):
        """
        Split multiple HTML pages into smaller documents by <h2> tags and convert them to plain text.
        More efficient implementation using direct node traversal instead of string operations.

        Args:
            soups: List of BeautifulSoup objects representing HTML documents

        Returns:
            list: List of plain text documents split at <h2> tags
        """
        documents = []

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=5000,
            chunk_overlap=200
        )

        for html in htmls:
            split = splitter.split_text(html)

            for doc in split:
                documents.append(doc)

        return documents


    def _extract_context_from_documents(self, query, documents, n_docs):
        """
        Extract context for the query from the most relevant documents.
        :param n: Number of documents to extract for context.
        :return: Context for LLM
        """
        n = min(n_docs, len(documents))  # Ensure 'n' is not larger than the number of documents

        doc_embeddings = self.model.encode(documents)
        query_embedding = self.model.encode([query])
        similarities = cosine_similarity(query_embedding, doc_embeddings)

        # Retrieve the most relevant documents
        top_n_indices = similarities.argsort()[0][-n:][::-1]
        top_n_documents = [documents[i] for i in top_n_indices]

        return "\n".join(top_n_documents)


    def get_context(self, query, max_sources=3, n_docs=3):
        hrefs = self._search_web_pages(query, max_sources)
        htmls = []

        for href in hrefs:
            htmls.append(self._parse_web_page(href))

        documents = self._split_htmls_into_documents(htmls)

        return self._extract_context_from_documents(query, documents, n_docs)


    def search_images(self, query, max_results=4):
        image_urls = []
        try:
            images = self.ddgs.images(query, max_results=max_results)

            for image in images:
                image_urls.append(image['image'])

        except Exception as e:
            print(e)

        return image_urls

    def search_videos(self, query, max_results=3):
        video_urls = []
        try:
            videos = self.ddgs.videos(query, max_results=max_results)

            for video in videos:
                video_urls.append(video['content'])

        except Exception as e:
            print(e)

        return video_urls



import asyncio
from crawl4ai import AsyncWebCrawler, CacheMode
from crawl4ai.extraction_strategy import CosineStrategy

def main():
    strategy = CosineStrategy(
        semantic_filter="what is blood altar",  # Content focus
        word_count_threshold=100,  # Minimum words per cluster
        sim_threshold=0.3,  # Similarity threshold
        max_dist=0.2,  # Maximum cluster distance
        top_k=1  # Number of top clusters to extract
    )

    async def extract(href):
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=href, strategy=strategy)
            print(result.extracted_content)

    query = "what is blood altar"
    href = "https://ftb.fandom.com/wiki/Blood_Altar"
    asyncio.run(extract(href))

if __name__ == "__main__":
    main()







