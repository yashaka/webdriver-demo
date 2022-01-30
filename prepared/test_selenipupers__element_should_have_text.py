from unittest import mock

import pytest
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

from givenpage import GivenPage
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ChromeOptions
import selenipupser as browser


@pytest.fixture(scope='function')
def with_browser_opened():
    options = ChromeOptions()
    # options.headless = True
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
    browser.driver = driver

    yield

    browser.driver.quit()


def test_have_inner_text(with_browser_opened):
    page = GivenPage(browser.driver)
    page.opened_with_body(
        '''
        <label>foobarfoo</label>
        '''
    )
    # before = time.time()
    # page.execute_script_with_timeout(
    #     '''
    #     document.getElementById('overlay').style.display = 'none';
    #     ''',
    #     250,
    # )

    browser.element('label').should_have_text('bar')

    # time_spent = time.time() - before
    # assert time_spent > 0.25
    assert "bar" in browser.driver.find_element_by_tag_name('foo').text


def test_have_full_text():
    webelement = mock.Mock(spec=WebElement)
    webelement.text = 'foobarfoo'

    browser.match_element_text_containing('foobarfoo')(webelement)


def test_have_empty_text_in_empty_text():
    webelement = mock.Mock(spec=WebElement)
    webelement.text = ''

    browser.match_element_text_containing('')(webelement)


def test_have_empty_text_in_non_empty_text():
    webelement = mock.Mock(spec=WebElement)
    webelement.text = 'something'

    browser.match_element_text_containing('')(webelement)


def test_have_no_some_text_in_empty_text():
    webelement = mock.Mock(spec=WebElement)
    webelement.text = 'something'

    try:
        browser.match_element_text_containing('')(webelement)

    except WebDriverException as error:
        assert 'Reason: actual text: «something»' in str(error)


def test_have_no_text_in_absent_webelement():
    webelement = mock.Mock(spec=WebElement)
    type(webelement).text = mock.PropertyMock(
        side_effect=NoSuchElementException(
            'no such element: Unable to locate element: '
            + '{"method":"css selector","selector":"foo"}'
        )
    )

    try:
        browser.match_element_text_containing('')(webelement)

    except NoSuchElementException as error:
        assert (
            'no such element: Unable to locate element: '
            + '{"method":"css selector","selector":"foo"}'
            in
            str(error)
        )
