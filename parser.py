import requests
from bs4 import BeautifulSoup
from lxml import etree

def parse_price(url, xpath):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Преобразуем BeautifulSoup-объект в lxml-дерево
    dom = etree.HTML(str(soup))

    # Ищем элемент по XPath
    price_element = dom.xpath(xpath)
    if price_element:
        price_text = price_element[0].text.strip()  # Берём первый найденный элемент
        # Очистка цены от лишних символов (например, валюты, пробелов)
        price = ''.join(filter(str.isdigit, price_text))
        return float(price) if price else None
    return None