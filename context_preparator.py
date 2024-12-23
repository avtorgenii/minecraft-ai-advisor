from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
import requests
from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.chrome.options import Options


ddgs = DDGS()

# Selenium oprtions
options = Options()
options.add_argument('--headless')  # Run in headless mode (no browser window)
options.add_argument('--disable-gpu')  # Disable GPU for headless mode
options.add_argument('--no-sandbox')  # Necessary for some systems (Linux-based)



def search_web_pages(query):
    return [res['href'] for res in ddgs.text(query, max_results=1)]



def selenium_search(href):
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(href)
        page_content = driver.page_source
    except WebDriverException:
        return None
    finally:
        driver.quit()

    return page_content


# TODO - deal with potential Nones by finding more related web pages, but not too much - after certain threshold just return that sources could not be found
def parse_web_page(href, for_craft=False):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }

    response = requests.get(href, headers=headers)

    html = response.text if response.status_code == 200 else selenium_search(href)

    if html is None:
        return None

    soup = BeautifulSoup(html, 'html.parser')

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

    else:
        return soup.get_text(separator=' ', strip=True)





if __name__ == '__main__':
    query = "how to craft blood altar"

    hrefs = search_web_pages(query)

    for href in hrefs:
        res = parse_web_page(href, for_craft=True)

