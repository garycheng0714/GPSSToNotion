from bs4 import BeautifulSoup
from selenium import webdriver
from lxml import etree
import pandas as pd
import os
import re
import requests
import shutil


def main():
    Patent('US20200120829A1')


class Patent:
    base_url = 'https://gpss4.tipo.gov.tw'

    def __init__(self, number):
        self.number = number
        self.url = f'https://gpss4.tipo.gov.tw/gpsskmc/gpssbkm?!!FRURL{number}'
        self.__driver = webdriver.Chrome(executable_path=os.getcwd() + '/chromedriver')

        try:
            self.__html = self.__get_html()
        finally:
            self.__driver.close()

    def __get_html(self):
        self.__driver.get(self.url)

        # with open('new_version_page.html', 'w') as f:
        #     f.write(self.__driver.page_source)

        # with open('new_version_page.html', 'r') as f:
        #     self.__html = f.read()

        return self.__driver.page_source

    def download_all_image(self):
        folder_path = os.path.join(os.getcwd(), 'image')

        if os.path.isdir(folder_path):
            shutil.rmtree(folder_path)

        os.makedirs(folder_path, exist_ok=True)

        image_download_urls = self.__get_all_image_download_url()

        if len(image_download_urls) > 0:
            for download_url in image_download_urls:
                file_name = os.path.basename(download_url).split("?")[0]

                resp = requests.get(download_url, stream=True)
                resp.raw.decode_content = True
                local_file = open(folder_path + '/' + file_name, 'wb')
                shutil.copyfileobj(resp.raw, local_file)

    def __get_all_image_download_url(self):
        soup = BeautifulSoup(self.__html, 'html.parser')

        tags = soup.find_all('img', {'src': re.compile(r'/gpssbkmusr/.*/.*')})

        return [self.base_url + tag['src'] for tag in tags]

    def get_data(self):
        soup = BeautifulSoup(self.__html, 'html.parser')
        table = soup.find('table', {'class': "table_2nd"})
        table_rows = table.find_all('tr')

        res = []

        for tr in table_rows:
            td = tr.find_all('td')
            row = [tr.text for tr in td]
            res.append(row)

        return pd.DataFrame(res)

    def get_patent_detail_text(self):
        selector = etree.HTML(self.__html)
        result = selector.xpath(self.__get_section_xpath('詳細說明'))
        if result:
            xml_content = etree.tostring(result[0], encoding="utf-8").decode('utf-8')
            detail_content_html = BeautifulSoup(xml_content, 'html.parser').find('div', {'class': 'panel-body'})
            return self.__remove_section_html_tag(detail_content_html)
        return None

    @staticmethod
    def __get_section_xpath(section_name):
        return f"""
                //h3[contains(text(), '{section_name}')]
                //parent::div[@class='panel-heading']
                //following-sibling::div[@class='panel-body']
               """

    @staticmethod
    def __remove_section_html_tag(html):
        text = str(html).replace('<br/>', '\n')
        text = re.sub(r'</div>', '', text)
        text = re.sub(r'<div .*>', '', text)
        return text

    def get_patent_range_text(self):
        selector = etree.HTML(self.__html)
        result = selector.xpath(self.__get_section_xpath('專利範圍'))
        if result:
            xml_content = etree.tostring(result[0], encoding="utf-8").decode('utf-8')
            patent_range_html = BeautifulSoup(xml_content, 'html.parser').find('div', {'class': 'panel-body'})
            return self.__remove_section_html_tag(patent_range_html)
        return None

    @property
    def name(self):
        soup = BeautifulSoup(self.__html, 'html.parser')
        return soup.find('td', {'class': 'TI'}).text

    @property
    def summary(self):
        soup = BeautifulSoup(self.__html, 'html.parser')
        summary_tag = soup.find('div', {'class': 'divsum_AB'})
        if summary_tag is not None:
            return summary_tag.text
        return None


if __name__ == "__main__":
    main()
