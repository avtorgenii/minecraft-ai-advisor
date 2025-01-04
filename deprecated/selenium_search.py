from selenium.webdriver.support import expected_conditions as EC


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time

from selenium.webdriver.support.wait import WebDriverWait


class SeleniumSearch:
    def __init__(self, wait_load_time=5):
        # Selenium web search options
        self.options = Options()
        self.options.add_argument('--headless')  # Run in headless mode (no browser window)
        self.options.add_argument('--disable-gpu')  # Disable GPU for headless mode
        self.options.add_argument('--no-sandbox')  # Necessary for some systems (Linux-based)
        self.options.add_argument('--mute-audio')  # Mute audio
        self.driver = webdriver.Chrome(options=self.options)
        self.wait_load_time = wait_load_time

    def __del__(self):
        # Close the driver upon deletion of the object
        try:
            self.driver.quit()
        except Exception:
            pass

    def handle_consent(self):
        # Handle Google's cookie consent banner
        try:
            consent_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept all')]"))
            )
            consent_button.click()
        except Exception as e:
            print("Consent widget not found or dismissed:", str(e))


    def text(self, query, max_results=10):
        """
        Perform a web search and return text-based results.

        :param query: Search query string.
        :param max_results: Maximum number of results to return.
        :return: A list of text-based search results (URLs).
        """
        self.driver.get('https://www.google.com/')

        self.handle_consent()

        # Find the search bar and input the search query
        search_box = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_box.send_keys(query)
        search_box.submit()

        # Wait for search results to load
        WebDriverWait(self.driver, self.wait_load_time).until(
            EC.presence_of_all_elements_located((By.XPATH, "//a[@href]"))
        )

        # Find search result links
        links = self.driver.find_elements(By.XPATH, "//a[@href]")

        results = []
        for link in links:
            href = link.get_attribute('href')
            if 'http' in href:  # Ensure it's a valid HTTP link
                results.append(href)
                if len(results) >= max_results:
                    break


        time.sleep(50)

        return results

    def images(self, query, max_results=10):
        """
        Perform an image search and return image result links.

        :param query: Search query string.
        :param max_results: Maximum number of results to return.
        :return: A list of image result links.
        """
        self.driver.get('https://www.google.com/imghp?hl=en')

        # Find the search bar and input the search query
        search_box = self.driver.find_element(By.NAME, "q")
        search_box.send_keys(query)
        search_box.submit()

        # Wait for search results to load
        self.driver.implicitly_wait(self.wait_load_time)

        # Find all <a> elements with href containing "/imgres" (image result links)
        links = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/imgres')]")

        images = []
        for link in links[:max_results]:
            href_value = link.get_attribute('href')
            images.append(href_value)

        return images

    def videos(self, query, max_results=10):
        """
        Perform a video search on YouTube and return video result links.

        :param query: Search query string.
        :param max_results: Maximum number of results to return.
        :return: A list of video result links.
        """
        self.driver.get('https://www.youtube.com/')

        # Find the search bar and input the search query
        search_box = self.driver.find_element(By.NAME, "search_query")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

        # Wait for search results to load
        self.driver.implicitly_wait(self.wait_load_time)

        # Find video result links
        links = self.driver.find_elements(By.XPATH, "//a[@id='video-title']")

        videos = []
        for link in links[:max_results]:
            href_value = link.get_attribute('href')
            videos.append(href_value)

        return videos




if __name__ == '__main__':
    ss = SeleniumSearch(wait_load_time=5)

    res = ss.text("blood altar in minecraft", 3)

    print(res)












