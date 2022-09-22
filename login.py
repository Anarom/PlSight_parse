from selenium.webdriver.common.keys import Keys
from get_driver import get_driver

def login():
    start_url = 'https://app.pluralsight.com/id?'
    search_url = 'https://app.pluralsight.com/search/?m_Sort=relevance&type=courses&page='
    driver = get_driver()
    driver.get(start_url)
    username = driver.find_element_by_css_selector('#Username')
    password = driver.find_element_by_css_selector('#Password')
    username.send_keys('EMAIL')
    password.send_keys('PASSWORD')
    password.send_keys(Keys.RETURN)
    return driver
