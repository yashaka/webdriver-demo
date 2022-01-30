from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as match
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver import ChromeOptions

options = ChromeOptions()
# options.headless = True
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
wait = WebDriverWait(driver, 4)

driver.get('https://duckduckgo.com/')

query = driver.find_element_by_xpath('//input[@name="q"]')
assert query.text == ''
assert query.get_attribute('value') == ''

query.send_keys('yashaka selene python' + Keys.ENTER)

results = driver.find_elements(By.CSS_SELECTOR, '.result__body')
assert len(results) > 5
assert 'User-oriented Web UI browser tests' in results[0].text

results[0].find_element(By.CSS_SELECTOR, 'a').click()
wait.until(match.title_contains('yashaka/selene'))

driver.quit()

