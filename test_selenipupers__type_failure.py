from givenpage import GivenPage
import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException

from selenium.webdriver import ChromeOptions

import duckgo
import selenipupser
from selenipupser import element, visit


options = ChromeOptions()
# options.headless = True
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)

selenipupser.driver = driver

page = GivenPage(driver)
page.opened_with_body(
        '''
        <input value="before"></input>
        <div 
            id='overlay' 
            style='
                display:block;
                position: fixed;
                display: block;
                width: 100%;
                height: 100%;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background-color: rgba(0,0,0,0.1);
                z-index: 2;
                cursor: pointer;
            '
        >
        </div>
        '''
)
before = time.time()


try:
    element('input').type(' after')
    raise AssertionError('should fail with error')

except TimeoutException as error:
    time_spent = time.time() - before
    assert time_spent > 4

    assert 'Message: failed trying to: type( after)' in str(error)
    assert (
        'Reason: element <input value="before"> '
        + 'is overlapped by <div id="overlay"'
        in str(error)
    )

    assert 'before' == driver.find_element_by_tag_name('input').get_attribute('value')

driver.quit()
