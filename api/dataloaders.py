from typing import List
from strawberry.dataloader import DataLoader
from strawberry.extensions import Extension
from sqlalchemy import select
from database import models as orm
from database.session import get_session
import enum

class DataLoaders(enum.Enum):
    brands = enum.auto()
    products = enum.auto()
    reviews_by_product = enum.auto()


async def load_brands(keys: List[int]) -> List[orm.Brand]:
    query = select(orm.Brand).where(orm.Brand.id.in_(keys))
    async with get_session() as session:
        brands = (await session.scalars(query)).all()
    brand_by_brand_id = {brand.id: brand for brand in brands}
    return [brand_by_brand_id.get(key) for key in keys]


async def load_products(keys: List[int]) -> List[orm.Product]:
    query = select(orm.Product).where(orm.Product.id.in_(keys))
    async with get_session() as session:
        products = (await session.scalars(query)).all()
    product_by_product_id = {product.id: product for product in products}
    return [product_by_product_id.get(key) for key in keys]


async def load_reviews_by_product(keys: List[int]) -> List[orm.Product]:
    query = select(orm.Review).where(orm.Review.product.in_(keys))
    async with get_session() as session:
        reviews = (await session.scalars(query)).all()
    product_dict = {}
    for review in reviews:
        if review.product not in product_dict:
            product_dict[review.product] = [review]
        else:
            product_dict[review.product].append(review)
    return [product_dict.get(key) for key in keys]


class DataLoadersExtension(Extension):
    def on_request_start(self):
        self.execution_context.context.update({
            DataLoaders.brands: DataLoader(load_brands),
            DataLoaders.products: DataLoader(load_products),
            DataLoaders.reviews_by_product: DataLoader(load_reviews_by_product),
        })