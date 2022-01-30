from __future__ import annotations

from typing import Callable, Tuple, List, Union
import re

from selenium.common.exceptions import WebDriverException, ElementNotInteractableException
from selenium.webdriver.android.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
# from selenium.webdriver.support.wait import WebDriverWait
from wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as match
from selenium.webdriver.common.action_chains import ActionChains

driver: WebDriver = ...


def visit(url):
    driver.get(url)


def wait():
    return WebDriverWait(
        driver,
        4,
        poll_frequency=0.1,
        ignored_exceptions=(WebDriverException,)
    )


def should_have_title_containing(value: str):
    wait().until(match.title_contains(value))


def quit():
    driver.quit()


def actions():
    return ActionChains(driver)


def _wait_until_passed(
        element: Element,
        command: Callable[[WebElement], None],
        description=''
):
    return wait().until(
        match_passed(element, command),
        message='failed trying to: ' + description
    )


def by(css_selector: str):
    return By.CSS_SELECTOR, css_selector


class match_element_is_visible(object):
    def __call__(self, webelement: WebElement):
        actual = webelement.is_displayed()
        if not actual:
            raise WebDriverException(
                stacktrace=[f'Reason: actual element is not displayed']
            )


class match_element_text_containing(object):
    def __init__(self, text):
        self.expected = text

    def __call__(self, webelement: WebElement):
        actual = webelement.text
        if self.expected not in actual:
            raise WebDriverException(
                stacktrace=[
                    f'Reason: actual text: «{actual}» '
                ]
            )


class match_value_of_element(object):
    def __init__(self, text):
        self.expected = text

    def __call__(self, webelement: WebElement):
        actual = webelement.get_attribute('value')
        if not self.expected == actual:
            raise WebDriverException(
                stacktrace=[f'Reason: \n'
                            f'\tactual value: «{actual}» \n'
                            f'\tis not equal to\n'
                            f'\texpected value: «{self.expected}»']
            )


class match_passed(object):
    def __init__(
            self,
            entity: Union[Element, Elements],
            command: Callable[[Union[WebElement, List[WebElement]]], None]
    ):
        self.entity = entity
        self.command = command

    def __call__(self, driver: WebDriver) -> bool:
        try:
            raw_entity = self.entity.locate()
            self.command(raw_entity)
            return True
        except Exception as error:
            reason = getattr(error, 'msg', str(error)) or str(error)
            raise WebDriverException(
                stacktrace=[
                    f'On: {self.entity}\n'
                    f'Reason: {reason}'
                ]
            )


class match_count_more_than(object):
    def __init__(self, value):
        self.expected = value

    def __call__(self, webelements: List[WebElement]):
        actual = len(webelements)
        if not actual > self.expected:
            raise WebDriverException(
                stacktrace=[f'Reason: \n'
                            f'\tactual amount: «{actual}» \n'
                            f'\tis not more than\n'
                            f'\texpected amount: «{self.expected}»']
            )


def _actual_not_overlapped_element(webelement):
    maybe_cover: WebElement = driver.execute_script(
        '''
                var element = arguments[0];
                
                var isVisible = !!( 
                    element.offsetWidth 
                    || element.offsetHeight 
                    || element.getClientRects().length 
                ) && window.getComputedStyle(element).visibility !== 'hidden'

                if (!isVisible) {
                    throw 'element is not visible'
                }

                var rect = element.getBoundingClientRect();
                var x = rect.left + rect.width/2;
                var y = rect.top + rect.height/2;

                var elementByXnY = document.elementFromPoint(x,y);
                if (elementByXnY == null) {
                    return null;
                }

                var isNotOverlapped = element.isSameNode(elementByXnY);
                
                return isNotOverlapped  ? null : elementByXnY;
        '''
        , webelement
    )
    if maybe_cover is not None:
        # todo: consider using AssertionError
        element_html = re.sub('\\s+', ' ', webelement.get_attribute("outerHTML"))
        cover_html = re.sub('\\s+', ' ', maybe_cover.get_attribute("outerHTML"))
        raise ElementNotInteractableException(
            stacktrace=[f'Reason: element {element_html} is overlapped by {cover_html}']
        )
    return webelement


class Locator(Callable[[], Union[WebElement, List[WebElement]]]):
    def __init__(
            self,
            func: Callable[[], Union[WebElement, List[WebElement]]],
            description: str
    ):
        self._func = func
        self._description = description

    def __call__(self) -> Union[WebElement, List[WebElement]]:
        return self._func()

    def __str__(self):
        return self._description


class Element:
    def __init__(self, locate: Locator):
        self.locate = locate

    def __str__(self):
        return str(self.locate)

    def element(self, selector) -> Element:
        return Element(Locator(
            lambda: self.locate().find_element(*by(selector)),
            f'{self}.element({selector})'
        ))

    # --- Asserts ---

    def should_be_visible(self) -> Element:
        wait().until(match_passed(self, match_element_is_visible()))
        return self

    def should_have_text(self, value) -> Element:
        _wait_until_passed(
            self,
            match_element_text_containing(value),
            f'assert match_element_text_containing({value})'
        )
        return self

    def should_have_value(self, value) -> Element:
        wait().until(match_passed(self, match_value_of_element(value)))
        return self

    def should_be_blank(self) -> Element:
        return self.should_have_text('').should_have_value('')

    # --- Commands ---

    def send_keys(self, keys) -> Element:
        _wait_until_passed(
            self,
            lambda its: its.send_keys(keys),
            description=f'type({keys})'
        )
        return self

    def type(self, keys) -> Element:
        _wait_until_passed(
            self,
            lambda its: _actual_not_overlapped_element(its).send_keys(keys),
            description=f'type({keys})'
        )
        return self

    def press_enter(self) -> Element:
        _wait_until_passed(
            self,
            lambda its: _actual_not_overlapped_element(its).send_keys(Keys.ENTER),
            description='press enter'
        )
        return self

    def click(self) -> Element:
        _wait_until_passed(
            self,
            lambda its: its.click(),
            description='click'
        )
        return self

    def clear(self) -> Element:
        _wait_until_passed(
            self,
            lambda its: _actual_not_overlapped_element(its).clear(),
            description='clear'
        )
        return self

    def double_click(self) -> Element:
        _wait_until_passed(
            self,
            lambda its: actions().double_click(its).perform(),
            description='double click'
        )
        return self

    def hover(self) -> Element:
        _wait_until_passed(
            self,
            lambda its: actions().move_to_element(its).perform(),
            description='hover'
        )
        return self


def element(selector) -> Element:
    return Element(Locator(
        lambda: driver.find_element(*by(selector)),
        f'element({selector})'
    ))


class Elements:

    def __init__(self, locate: Locator):
        self.locate = locate

    def __str__(self):
        return self.locate.__str__()

    # --- Element builders ---

    @property
    def first(self) -> Element:
        return self[0]

    @property
    def second(self) -> Element:
        return self[1]

    def __getitem__(self, index: int) -> Element:
        return Element(Locator(
            lambda: self.locate()[index],
            f'{self}[{index}]'
        ))

    # --- Asserts ---

    def should_have_count_more_than(self, value: int) -> Elements:
        wait().until(match_passed(self, match_count_more_than(value)))
        return self


def elements(selector) -> Elements:
    return Elements(Locator(
        lambda: driver.find_elements(*by(selector)),
        f'elements({selector})'
    ))
