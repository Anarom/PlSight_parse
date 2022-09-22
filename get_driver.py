from selenium import webdriver

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome('C:\\Python\\chromedriver.exe',options = options)
    return driver
