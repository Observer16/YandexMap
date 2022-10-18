import requests
from selenium import webdriver
import time
import csv
from datetime import datetime
from bs4 import BeautifulSoup
from lxml import html
from proxy_config import login, password, proxy
from selenium.webdriver.common.by import By
requests.packages.urllib3.disable_warnings()

request = "еда москва"
url = ('https://yandex.ru/maps/11030/azov/search/' + request + '/')

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 OPR/83.0.4254.62',
    'Accept': '*/*'
    
}

proxies = {
    'https': f'http://{login}:{password}@{proxy}'
}

# Манипуляции с скролингом страницы
def scroll(url):
        driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(5)
        driver.implicitly_wait(15)

        element = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[9]/div[2]/div[1]/div[1]/div[1]/div/div[1]/div/div/div[4]')
        driver.execute_script("arguments[0].scrollIntoView(true);", element);
        time.sleep(5)

        #while True:
        a = 1
        while a < 60:
            
            driver.execute_script("arguments[0].scrollIntoView(true);", element);
            time.sleep(8)        
            driver.execute_script("return document.body.scrollHeight")

            a += 1
            if a == 59:
	            break

        #cur_date = datetime.now().strftime('%m_%d_%Y')
        table_href = []

        soup = BeautifulSoup(driver.page_source, 'lxml')
        firm = soup.find_all("a", class_="search-snippet-view__link-overlay")
        for link in firm:
            href_date = (link.get('href'))
            table_href.append(href_date)

        with open(file=f'YandexMap/data_{request}.csv', mode='a') as file:
            writer = csv.writer(file)
            for item in table_href:
                writer.writerow([item])   

def get_data(url):
    cur_date = datetime.now().strftime('%m_%d_%Y')
    response = requests.get(url=url, headers=headers)
    print(response)
    

    with open(file='YandexMap/index.html', mode='w') as file:
        file.write(response.text)

    with open(file='YandexMap/index.html') as file:
        src = file.read()

    table_href = []

    soup = BeautifulSoup(src, 'lxml')
    firm = soup.find_all("a", class_="search-snippet-view__link-overlay")
    for link in firm:
        href_date = (link.get('href'))
        table_href.append(href_date)
     
    with open(file=f'YandexMap/data_{cur_date}.csv', mode='a') as file:
        writer = csv.writer(file)
        for item in table_href:
            writer.writerow([item])


def main():
    #url = ('https://yandex.ru/maps/11030/azov/search/ремонт/?ll=39.416338%2C47.097289&sll=39.416338%2C47.097289&sspn=0.060060%2C0.063902&utm_source=main_stripe_big&z=13.61')
    scroll(url)
    #get_data(url)
    time.sleep(5)    
    #download_xlsx()
    
if __name__ == '__main__':
    main()