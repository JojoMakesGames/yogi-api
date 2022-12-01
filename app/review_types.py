import typing
import strawberry
from strawberry.types import Info
from app.dataloaders import DataLoaders

@strawberry.interface
class ReviewSearchFilter:
    id: strawberry.ID
    name: str

@strawberry.type
class ReviewSearchBrand(ReviewSearchFilter):
    id: strawberry.ID
    name: str

    @strawberry.field
    async def review_count(self, info: Info) -> int:
        return await info.context[DataLoaders.brands].load(self.brand)

@strawberry.type
class ReviewSearchProduct(ReviewSearchFilter):
    brand_id: strawberry.Private[int]

    id: strawberry.ID
    name: str
    views: int
    brand: ReviewSearchBrand
    review_count: int
    average_review: float

    @strawberry.field
    async def brand(self, info: Info) -> ReviewSearchBrand:
        brand = await info.context[DataLoaders.brands].load(self.brand_id)
        return ReviewSearchBrand(id=brand.id, name=brand.name)

    @strawberry.field
    async def review_count(self, info: Info) -> int:
        reviews = await info.context[DataLoaders.reviews_by_product].load(self.id)
        return len(reviews) if reviews else 0

    @strawberry.field
    async def average_review(self, info: Info) -> float:
        reviews = await info.context[DataLoaders.reviews_by_product].load(self.id)
        return sum([review.rating for review in reviews])/len(reviews) if reviews else 0

@strawberry.type
class ReviewSearchFilters:
    products: typing.List[ReviewSearchFilter]
    brands: typing.List[ReviewSearchFilter]

@strawberry.type
class ReviewSearch:
    filters: ReviewSearchFilters
    unique_products: typing.List[ReviewSearchProduct]