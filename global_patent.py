from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import os


def main():

    data = Patent('D203134').get_data()
    print(data)
    print(data.shape[0])
    # print(data.iloc[0].values[0])
    # for row in data:
    #     print(row)
    #     print(row.values[0])


class Patent:
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    def __init__(self, number):
        self.number = number
        self.url = f'https://twpat7.tipo.gov.tw/tipotwoc/tipotwkm?!!FR_{number}'
        self.__html = None
        self.__driver = webdriver.Chrome(
            executable_path=os.getcwd() + '/chromedriver',
            chrome_options=self.chrome_options
        )
        self.__get_html()

    def __wait(self, locator):
        try:
            WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            print('exception')

    def __get_html(self):
        self.__driver.get("https://gpss.tipo.gov.tw/")

        self.__wait_search_bar_shown()
        self.__search_patent()
        self.__wait_search_result_shown()
        self.__click_patent_link()

        self.__html = self.__driver.page_source

        self.__driver.close()

    def __search_patent(self):
        input_field = self.__driver.find_element_by_name('_21_1_T')
        input_field.send_keys(self.number)
        search_button = self.__driver.find_element_by_name('_IMG_檢索')
        search_button.click()

    def __wait_search_bar_shown(self):
        self.__wait((By.NAME, "_21_1_T"))

    def __wait_search_result_shown(self):
        self.__wait((By.CLASS_NAME, "sumtd2_PN"))

    def __click_patent_link(self):
        patent = self.__driver.find_element_by_link_text(f'TW{self.number}')
        patent.click()

    def __get_soup(self):
        return BeautifulSoup(self.__html, 'html.parser')

    def get_data(self):
        table = self.__get_soup().find('table', {'class': "table_2nd"})
        table_rows = table.find_all('tr')

        res = []

        for tr in table_rows:
            td = tr.find_all('td')
            row = [tr.text for tr in td]
            res.append(row)

        return pd.DataFrame(res)

    def get_name(self):
        return self.__get_soup().find('td', {'class': 'TI'}).text

    def get_summary(self):
        return self.__get_soup().find('div', {'class': 'divsum_AB'}).text


if __name__ == "__main__":
    main()
