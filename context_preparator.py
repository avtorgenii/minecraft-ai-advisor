from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
import requests
from langchain_text_splitters import RecursiveCharacterTextSplitter
from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.chrome.options import Options
from encoder import load_st
from sklearn.metrics.pairwise import cosine_similarity


class ContextPreparator:
    def __init__(self):
        # Duckduck go web search
        self.ddgs = DDGS()

        # Selenium web search options
        self.options = Options()
        self.options.add_argument('--headless')  # Run in headless mode (no browser window)
        self.options.add_argument('--disable-gpu')  # Disable GPU for headless mode
        self.options.add_argument('--no-sandbox')  # Necessary for some systems (Linux-based)
        self.driver = webdriver.Chrome(options=self.options)

        # Sentence encoder for extracting context
        self.model = load_st()

    def _search_web_pages(self, query):
        """Search for web pages using DuckDuckGo."""
        return [res['href'] for res in self.ddgs.text(query, max_results=1)]

    def _selenium_search(self, href):
        """Use Selenium to extract page content."""
        try:
            self.driver.get(href)
            page_content = self.driver.page_source
        except WebDriverException:
            return None
        return page_content

    def _parse_web_page(self, href, for_craft=True):
        """
        Parse the web page and extract text content.
        If for_craft is True, extract items for crafting.
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        }

        response = requests.get(href, headers=headers)
        html = response.text if response.status_code == 200 else self._selenium_search(href)

        if html is None:
            return None

        soup = BeautifulSoup(html, 'html.parser')

        # Handle crafting-specific page parsing
        if for_craft:
            a_elements = soup.find_all('a', attrs={'title': True})
            span_elements = soup.find_all('span', attrs={'title': True})

            for a in a_elements:
                p_tag = soup.new_tag('p')
                p_tag.string = a['title']
                a.replace_with(p_tag)

            for span in span_elements:
                p_tag = soup.new_tag('p')
                p_tag.string = span['title']
                span.replace_with(p_tag)

            return soup.get_text(separator=' ', strip=True)

        return soup.get_text(separator=' ', strip=True)

    def _split_pages_into_documents(self, pages):
        """
        Split multiple pages into smaller documents using a recursive character text splitter.
        """
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=200
        )

        documents = []

        for page in pages:
            split = splitter.split_text(page)
            documents.extend(split)

        return documents

    def _extract_context_from_documents(self, query, documents, n=2):
        """
        Extract context for the query from the most relevant documents.
        :param n: Number of documents to extract for context.
        :return: Context for LLM
        """
        n = min(n, len(documents))  # Ensure 'n' is not larger than the number of documents

        doc_embeddings = self.model.encode(documents)
        query_embedding = self.model.encode([query])
        similarities = cosine_similarity(query_embedding, doc_embeddings)

        # Retrieve the most relevant documents
        top_n_indices = similarities.argsort()[0][-n:][::-1]
        top_n_documents = [documents[i] for i in top_n_indices]

        return "\n".join(top_n_documents)


    def get_context(self, query):
        hrefs = self._search_web_pages(query)
        pages = []

        for href in hrefs:
            pages.append(self._parse_web_page(href))

        documents = self._split_pages_into_documents(pages)

        return self._extract_context_from_documents(query, documents)


    def search_images(self, query):
        image_urls = None
        try:
            image_urls = self.ddgs.images(query, max_results=2)
        except Exception as e:
            print(e)

        return image_urls





if __name__ == '__main__':
    query = "how to craft blood altar in ftb evolved"

    cp = ContextPreparator()

    context = cp.get_context(query)

    print(context)


