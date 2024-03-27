from unittest import TestCase
from unittest.mock import MagicMock, patch

import requests
from bs4 import BeautifulSoup

from services.service import LinksParser, XmlExtractor


class LinksParserTestCase(TestCase):

    def test_parse_links_method_when_all_ok(self):
        parser = LinksParser(1)
        links = parser.parse_links()
        self.assertEqual(10, len(links))

    def test_prepare_links_method_when_invalid_page_then_return_first_page(self):
        parse = LinksParser('someinvalidpage')
        links = parse.parse_links()
        self.assertEqual(10, len(links))

    @patch('requests.get')
    def test_parse_page_soup_success_response(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
            <html>
                <body>
                    <div class="registry-entry__header-mid__number">
                        <a href="...regNumber=123">...</a>
                    </div>
                </body>
            </html>
            """
        mock_get.return_value = mock_response
        parser = LinksParser(1)
        soup = parser.parse_page_soup()
        self.assertIsInstance(soup, BeautifulSoup)
        self.assertEqual(len(soup.find_all('div', class_='registry-entry__header-mid__number')), 1)

    @patch('requests.get')
    def test_parse_page_soup_error_response(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        parser = LinksParser(1)
        with self.assertRaises(requests.HTTPError):
            parser.parse_page_soup()


class XmlExtractorTests(TestCase):

    @patch('requests.get')
    def test_parse_xml_content_to_dict_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
        <root>
            <data>Some data</data>
        </root>
        """
        mock_get.return_value = mock_response
        extractor = XmlExtractor('https://mocklink.com')
        xml_dict = extractor.parse_xml_content_to_dict()
        self.assertIsInstance(xml_dict, dict)
        self.assertEqual(xml_dict['root']['data'], 'Some data')

    @patch('requests.get')
    def test_parse_xml_content_to_dict_failure(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        extractor = XmlExtractor('https://mocklink.com')
        with self.assertRaises(requests.HTTPError):
            extractor.parse_xml_content_to_dict()

    @patch('services.service.XmlExtractor.parse_xml_content_to_dict')
    def test_extract_dti_from_dict(self, mock_parse_dict):
        mock_dict = {
            'root': {
                'commonInfo': {
                    'publishDTInEIS': '2024-03-26'
                }
            }
        }
        mock_parse_dict.return_value = mock_dict
        extractor = XmlExtractor('https://mocklink.com')
        dti = extractor.extract_dti_from_dict(mock_dict)
        self.assertEqual(dti, 'https://mocklink.com - 2024-03-26')

    @patch('services.service.XmlExtractor.parse_xml_content_to_dict')
    def test_extract_dti(self, mock_parse_dict):
        mock_dict = {
            'root': {
                'commonInfo': {
                    'publishDTInEIS': '2024-03-26'
                }
            }
        }
        mock_parse_dict.return_value = mock_dict
        extractor = XmlExtractor('https://mocklink.com')
        dti = extractor.extract_dti()
        self.assertEqual(dti, 'https://mocklink.com - 2024-03-26')
