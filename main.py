from datetime import date
import re
from attr import attrs
from bs4 import BeautifulSoup as beauty
import cloudscraper
import pandas as pd
from product_type import ProductType

def formatNumber(text: str) -> float:
    numeros = re.findall(r'\d+', text)
    formatado = ''.join(numeros[:-1])
    return float(formatado + '.' + numeros[-1])

scraper = cloudscraper.create_scraper(delay=10, browser='chrome') 
url = "https://www.terabyteshop.com.br/hardware/placas-de-video/nvidia-geforce"

info = scraper.get(url).text
soup = beauty(info, "html.parser")
products = soup.find_all('div', attrs={'class': 'commerce_columns_item_inner'})

result = []
for idx, product in enumerate(products):
    esgotado = product.find('div', attrs={'class': 'commerce_columns_item_info'}).find('div', attrs={'class': 'tbt_esgotado'})
    # Somente os produtos que não estão esgotados, pois os esgotados não tem preço
    if esgotado is None:
        product_name = product.find('a', attrs={'class': 'prod-name'}).find('h2').text
        product_price = product.find('div', attrs={'class': 'commerce_columns_item_info'}).find('div', attrs={'class': 'prod-new-price'}).text
        product_url = product.find('a', attrs={'class': 'prod-name'})['href']

        result.append({
            ProductType.PRODUCT_NAME.value: product_name,
            ProductType.PRODUCT_PRICE.value: formatNumber(product_price),
            ProductType.PRODUCT_DATE.value: date.today(),
            ProductType.PRODUCT_SITE.value: url,
            ProductType.PRODUCT_URL.value: product_url,
        })

df = pd.DataFrame(result, columns = ProductType.list())
df.to_csv('terabyte.csv', index=False)