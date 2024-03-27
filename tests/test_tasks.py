import unittest
from unittest.mock import patch

import requests

from celery_app import ExtractXmlTask, ParseLinksTask
from celery_app import app as celery_app


class TasksTestCase(unittest.TestCase):

    def setUp(self):
        celery_app.conf.update({'CELERY_ALWAYS_EAGER': True})

    @patch('services.service.LinksParser.parse_links')
    def test_parse_links_task(self, mock_parse_links):
        mock_parse_links.return_value = ['https://mocklink.com', 'https://mocklink2.com']
        task = ParseLinksTask()
        result = task.run(1)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertTrue(all(isinstance(item, str) for item in result))

    @patch('services.service.XmlExtractor.extract_dti')
    def test_extract_xml_task(self, mock_extract_dti):
        mock_extract_dti.return_value = 'dti_data'
        task = ExtractXmlTask()
        result = task.run('link1')
        self.assertIsInstance(result, str)
        self.assertEqual(result, 'dti_data')

    @patch('services.service.LinksParser.parse_links')
    def test_parse_links_task_error(self, mock_parse_links):
        mock_parse_links.side_effect = Exception()
        task = ParseLinksTask()
        with self.assertRaises(Exception):
            task.run(1)

    @patch('requests.get')
    def test_extract_xml_task_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException()
        task = ExtractXmlTask()
        with self.assertRaises(requests.exceptions.RequestException):
            task.run('link1')
