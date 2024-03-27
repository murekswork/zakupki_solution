import logging

from celery import Task

from services.service import LinksParser, XmlExtractor


class ParseLinksTask(Task):
    name = 'parse_links'
    default_retry_delay = 5
    max_retries = 5

    def run(self, page: int):
        try:
            p = LinksParser(page)
            links = p.parse_links()
            result = []
            for link in links:
                dti = ExtractXmlTask().apply_async((link,))
                result.append(dti.id)
            return result
        except Exception as exc:
            logging.error('Connection error occured, retring! %s', exc)
            self.retry()


class ExtractXmlTask(Task):
    name = 'extract_xml'
    default_retry_delay = 5
    max_retries = 5

    def run(self, link: str):
        try:
            extractor = XmlExtractor(link)
            result = extractor.extract_dti()
            return result
        except Exception as exc:
            logging.error('Connection error occured, retring! %s', exc)
            self.retry()
