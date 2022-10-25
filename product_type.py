from enum import Enum

class ExtendedEnum(Enum):

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

class ProductType(ExtendedEnum):
    PRODUCT_NAME = 'product_name'
    PRODUCT_PRICE = 'product_price'
    PRODUCT_DATE = 'product_date'
    PRODUCT_SITE = 'product_site'
    PRODUCT_URL = 'product_url'