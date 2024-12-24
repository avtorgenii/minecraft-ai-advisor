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
        # Duckduck go web search for images
        self.ddgs = DDGS()

        # Selenium web search options
        self.options = Options()
        self.options.add_argument('--headless')  # Run in headless mode (no browser window)
        self.options.add_argument('--disable-gpu')  # Disable GPU for headless mode
        self.options.add_argument('--no-sandbox')  # Necessary for some systems (Linux-based)
        self.driver = webdriver.Chrome(options=self.options)

        # Sentence encoder for extracting context
        self.model = load_st()


    def __del__(self):
        try:
            self.driver.close()
        except ImportError:
            pass


    def _search_web_pages(self, query, max_results=2):
        """Search for web pages using DuckDuckGo."""
        return [res['href'] for res in self.ddgs.text(query, max_results=max_results)]

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

        # Handle crafting-specific page parsing
        if for_craft:
            crafting_grid_divs = soup.find_all('div', class_='CraftingGrid')

            # Iterate over each CraftingGrid div separately
            for crafting_grid_div in crafting_grid_divs:
                p_tag = soup.new_tag('p')
                p_tag.string = 'CRAFTING RECIPE:'

                # Insert the <p> tag before the CraftingGrid div
                crafting_grid_div.insert_before(p_tag)

                # Find all gridItemContainer divs inside the current CraftingGrid div
                grid_items = crafting_grid_div.find_all('div', class_='gridItemContainer')

                # Dictionary to count the occurrences of each ingredient
                ingredient_count_dict = {}

                # Iterate over each gridItemContainer and count the occurrences of ingredients
                for item in grid_items:
                    # Find the span element with the title attribute and no class attribute (i.e., ingredient)
                    title_spans = item.find_all('span', title=True, class_=False, recursive=True)

                    # Count occurrences of each ingredient
                    for title_span in title_spans:
                        ingredient = title_span['title']
                        if ingredient in ingredient_count_dict:
                            ingredient_count_dict[ingredient] += 1
                        else:
                            ingredient_count_dict[ingredient] = 1

                # After counting ingredients, replace spans with ingredient-count pairs
                for ingredient, count in ingredient_count_dict.items():
                    p_tag = soup.new_tag('p')
                    p_tag.string = f"{ingredient} x{count}"  # Pair with count

                    # Insert the new <p> tag for each ingredient
                    crafting_grid_div.insert_before(p_tag)

                # Optionally, remove the original gridItemContainer divs after processing
                for item in grid_items:
                    item.extract()

            return soup
        else:
            return soup

    def _split_htmls_into_documents(self, soups):
        """
        Split multiple HTML pages into smaller documents by <h2> tags and convert them to plain text.
        More efficient implementation using direct node traversal instead of string operations.

        Args:
            soups: List of BeautifulSoup objects representing HTML documents

        Returns:
            list: List of plain text documents split at <h2> tags
        """
        documents = []

        for soup in soups:
            # Find all <h2> tags
            h2_tags = soup.find_all('h2')

            if not h2_tags:
                # If no h2 tags, process the entire document as one piece
                documents.append(soup.get_text(separator=' ', strip=True))
                continue

            # Process document segments between h2 tags
            current_h2 = None
            for next_h2 in h2_tags:
                if current_h2 is None:
                    # Handle content before first h2
                    content = []
                    node = soup.find(recursive=False)
                    while node and node != next_h2:
                        if node.name != 'h2':
                            content.append(node.get_text(separator=' ', strip=True))
                        node = node.next_sibling
                    if content:
                        documents.append(' '.join(content))
                else:
                    # Handle content between h2 tags
                    content = []
                    node = current_h2.next_sibling
                    while node and node != next_h2:
                        content.append(node.get_text(separator=' ', strip=True))
                        node = node.next_sibling
                    documents.append(f"{current_h2.get_text()} {' '.join(content)}")

                current_h2 = next_h2

            # Handle content after last h2
            if current_h2:
                content = []
                node = current_h2.next_sibling
                while node:
                    content.append(node.get_text(separator=' ', strip=True))
                    node = node.next_sibling
                documents.append(f"{current_h2.get_text()} {' '.join(content)}")

        return documents


    def _extract_context_from_documents(self, query, documents, n_docs=1):
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


    def get_context(self, query, max_sources=2, n_docs=2, for_craft=False):
        hrefs = self._search_web_pages(query, max_sources)
        htmls = []

        for href in hrefs:
            htmls.append(self._parse_web_page(href, for_craft))

        documents = self._split_htmls_into_documents(htmls)

        return self._extract_context_from_documents(query, documents, n_docs)


    def search_images(self, query, max_results=2):
        image_urls = None
        try:
            image_urls = self.ddgs.images(query, max_results=max_results)
        except Exception as e:
            print(e)

        return image_urls





if __name__ == '__main__':
    query = "how to craft tin cable"

    cp = ContextPreparator()

    context = cp.get_context(query, True)

    print(context)

    # parsed = cp._parse_web_page("https://ftb.fandom.com/wiki/Blood_Altar", False)
    #
    # print(parsed)




