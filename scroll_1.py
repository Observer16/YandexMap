import time
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Chrome()
driver.implicitly_wait(30)
url = ('https://yandex.ru/maps/11030/azov/search/ремонт/?ll=39.416338%2C47.097289&sll=39.416338%2C47.097289&sspn=0.060060%2C0.063902&utm_source=main_stripe_big&z=13.61')

try:
    SCROLL_PAUSE_TIME = 0.5
    driver.get(url)

    element = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[9]/div[2]/div[1]/div[1]/div[1]/div/div[1]/div/div/div[5]/h1')
    last_height = driver.execute_script("arguments[0].scrollIntoView(true);", element)

    while True:
        driver.execute_script("window.scrollTo(0, arguments[0].scrollIntoView(true));")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("arguments[0].scrollIntoView(true);")
        if new_height == last_height:
            break
        last_height = new_height

    soup = BeautifulSoup(driver.page_source, "html.parser")

    for c in soup("h2"):
        print(c.get_text())

finally:
    driver.quit()