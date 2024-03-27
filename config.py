from dataclasses import dataclass


@dataclass
class Config:
    PAGE_LINK = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?fz44=on&pageNumber={}'

    XML_LINK = 'https://zakupki.gov.ru/epz/order/notice/printForm/viewXml.html?regNumber={}'

    HEADERS = {
        'Cache-Control': 'no-cache',
        'Cookie': 'doNotAdviseToChangeLocationWhenIosReject=true; _ym_uid=1711448876506980460; _ym_d=1711448876; _ym_isad=1; _ym_visorc=b',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
    }
