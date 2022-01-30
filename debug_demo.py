from selene import be, have
from selene.support.shared import browser
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

browser.open('https://duckduckgo.com/')
browser.open('https://google.com/ncr')

browser.element('[name=query]').should(be.blank).type('yashaka selene python').press_enter()

browser.element('[name=q]')().get_attribute('outerHTML')


# noinspection PyStatementEffect

# limited to
expected_conditions.element

browser.driver.find_element_by_xpath("//*[@id='search-results']//a[contains(text(),'selenide.org')]")

(
    browser.all("#todo-list>li")
           .filtered_by(have.text("give talk"))
           .element(".toggle")
           .click()
)

browser.element("#new-todo").type("a").press_enter()

new_todo = browser.element("#new-todo")
todos = browser.all("#todo-list>li")

browser.open("http://todomvc.com/examples/emberjs/")

new_todo.type("give talk").press_enter()
new_todo.type("have fun").press_enter()


todos.should(have.te("give talk", "have fun"))



from selene.support.shared import browser as shared_browser

class TodoMVC:
    def __init__(self, browser=shared_browser):
        self.new_todo = browser.element("#new-todo")
        self.todos = browser.all("#todo-list>li")




