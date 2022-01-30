from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver import ChromeOptions
import selenipupser as browser

query = browser.element('[name=q]')
results = browser.elements('.result__body')

options = ChromeOptions()
# options.headless = True
driver = webdriver.Chrome(
    executable_path=ChromeDriverManager().install(),
    options=options
)

browser.driver = driver

# --- Test ---

browser.visit('https://duckduckgo.com/')

query.should_be_blank()\
    .type('github yashaka selene').press_enter()

results.should_have_count_more_than(5)\
    .second.should_have_text('Consise API to Selenium')\
    .element('.result__title').click()

browser.should_have_title_containing('yashaka/NSelene')

browser.quit()
