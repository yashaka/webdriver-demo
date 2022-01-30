import time
from unittest import mock

import pytest
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
from selenium.webdriver import ChromeOptions
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager

import selenipupser as browser
from givenpage import GivenPage
from selenipupser import match_element_text_containing, match_passed


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

    browser.element('label').should_have_text('oobarfo')

    assert 'oobarfo' in browser.driver.find_element_by_tag_name('label').text


def test_have_no_inner_text(with_browser_opened):
    page = GivenPage(browser.driver)
    page.opened_with_body(
        '''
        <label>foobarfoo</label>
        '''
    )
    before = time.time()

    try:
        browser.element('label').should_have_text('.obarf.')
        pytest.fail('should fail with error')

    except TimeoutException as error:
        time_spent = time.time() - before
        assert time_spent > 4

        assert 'Reason: actual text: «foobarfoo»' in str(error)


@pytest.fixture(scope='function')
def webelement_mock():
    yield mock.Mock(spec=WebElement)


def test_have_full_text(webelement_mock):
    webelement_mock.text = 'foobarfoo'

    match_element_text_containing('foobarfoo')(webelement_mock)


def test_have_empty_text_in_some_text(webelement_mock):
    webelement_mock.text = 'foobarfoo'

    match_element_text_containing('')(webelement_mock)


def test_have_empty_text_in_empty_text(webelement_mock):
    webelement_mock.text = ''

    match_element_text_containing('')(webelement_mock)


def test_have_no_some_text_in_empty_text(webelement_mock):
    webelement_mock.text = ''

    try:
        match_element_text_containing('something')(webelement_mock)
        pytest.fail('should fail with error')

    except WebDriverException as error:
        webelement_mock.assert_called_once()
        assert 'Reason: actual text: «»' in str(error)


def test_have_no_some_text_in_absent_element():
    driver = mock.Mock()
    element = mock.Mock()
    element.locate.side_effect = NoSuchElementException('no such element')

    try:
        match_passed(element, match_element_text_containing('something'))(driver)
        pytest.fail('should fail with error')

    except WebDriverException as error:
        assert 'Reason: no such element' in str(error)
