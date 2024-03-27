import requests
import xmltodict
from bs4 import BeautifulSoup

from config import Config
from decorators import time_loger


class LinksParser:

    def __init__(self, page: int):
        self.page = page

    @time_loger
    def parse_page_soup(self) -> BeautifulSoup:
        """
        Parse page, create and return bs4 object.
        """
        url = Config.PAGE_LINK.format(self.page)
        response = requests.get(url=url, headers=Config.HEADERS)
        if response.status_code != 200:
            raise requests.HTTPError('404')
        soup = BeautifulSoup(response.text)
        return soup

    @time_loger
    def parse_registry_numbers_from_soup(self, page: BeautifulSoup) -> list[str]:
        """
        Extract registry numbers from parsed soup object.
        """
        registry_divs = page.find_all(name='div', class_='registry-entry__header-mid__number')
        reg_numbers = []
        for div in registry_divs:
            number = div.find('a').get('href').split('regNumber=')[1]
            reg_numbers.append(number)
        return reg_numbers

    @time_loger
    def prepare_links(self, registry_numbers: list[str]) -> list[str]:
        """
        Create xml links based on registry numbers.
        """
        links = []
        for number in registry_numbers:
            links.append(Config.XML_LINK.format(number))
        return links

    @time_loger
    def parse_links(self) -> list[str]:
        """
        Start link parsing process: fetches HTML, extracts numbers, and prepares XML links.
        """
        soup = self.parse_page_soup()
        numbers = self.parse_registry_numbers_from_soup(soup)
        links = self.prepare_links(numbers)
        return links


class XmlExtractor:

    def __init__(self, link: str):
        self.link = link

    @time_loger
    def parse_xml_content_to_dict(self) -> dict:
        """
        Fetches XML content from the link and parses it to dict.
        """
        response = requests.get(self.link, headers=Config.HEADERS)
        if response.status_code != 200:
            raise requests.HTTPError('404')
        xml_dict = xmltodict.parse(response.text)
        return xml_dict

    @time_loger
    def extract_dti_from_dict(self, xml_dict: dict) -> str:
        """
        Extracts publishDTInEIS data from parsed XML dictionary.
        """
        dti = xml_dict[tuple(xml_dict.keys())[0]]['commonInfo'].get('publishDTInEIS', None)
        return f'{self.link} - {dti}'

    @time_loger
    def extract_dti(self) -> str:
        """
        Start xml parsing and publishDTInEIS extraction, return formatted string.
        """
        xml_dict = self.parse_xml_content_to_dict()
        dti = self.extract_dti_from_dict(xml_dict)
        return dti
