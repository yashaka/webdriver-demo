from selene import be, have
from selene.support.shared import browser

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver import ChromeOptions

import duckgo
import selenipupser
from selenipupser import element, visit


options = ChromeOptions()
# options.headless = True
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)

selenipupser.driver = driver

visit('https://the-internet.herokuapp.com/add_remove_elements/')

element('[onclick^=addElement]').click()
element('[onclick^=deleteElement]').click()

driver.quit()
