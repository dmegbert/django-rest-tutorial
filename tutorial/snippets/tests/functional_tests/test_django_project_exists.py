from selenium import webdriver


def test_api_site_is_up():
    browser = webdriver.Chrome(executable_path='/Users/degbert/.chrome/chromedriver')
    browser.get('http://localhost:8000')
    title = browser.title

    assert 'Api Root – Django REST framework' == title
