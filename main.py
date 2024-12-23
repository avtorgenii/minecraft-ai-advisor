from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Set Chrome options
options = Options()
options.add_argument('--headless')  # Run in headless mode (no browser window)
options.add_argument('--disable-gpu')  # Disable GPU for headless mode
options.add_argument('--no-sandbox')  # Necessary for some systems (Linux-based)

# Path to your ChromeDriver (make sure to provide the correct path to chromedriver)
driver = webdriver.Chrome(options=options)

# Navigate to the webpage
driver.get('https://minecraft.wiki/w/Stone_Sword')

# Get the page content
page_content = driver.page_source

# Close the browser
driver.quit()

# Print the page content (or do any other processing)
print(page_content)
