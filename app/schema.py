import strawberry

from fastapi import Depends
from strawberry.fastapi import GraphQLRouter
from strawberry.types import Info

from app.review_types import ReviewSearch, ReviewSearchBrand, ReviewSearchFilters, ReviewSearchProduct

from app.database.session import get_session
from app.database import models as orm

from app.dataloaders import DataLoaders, DataLoadersExtension

from sqlalchemy import select


@strawberry.type
class Query:
    @strawberry.field
    async def review_search(self, info: Info) -> ReviewSearch:
        query = select(orm.Product)
        async with info.context['session'] as session:
            products = (await session.scalars(query)).all()

        brands = await info.context[DataLoaders.brands].load_many([product.brand for product in products])
        brand_filters = [ReviewSearchBrand(id=brand.id, name=brand.name) for brand in set(brands)]
        products = [
            ReviewSearchProduct(
                id=product.id,
                name=product.name,
                views=product.views if product.views else 0,
                brand_id=product.brand
                ) for product in products]
        filters = ReviewSearchFilters(products=products, brands=brand_filters)

        return ReviewSearch(unique_products=products, filters=filters)

async def get_context(
    session=Depends(get_session),
):
    return {
        "session": session,
    }

schema = strawberry.Schema(query=Query, extensions=[DataLoadersExtension])

graphql_app = GraphQLRouter(schema, context_getter=get_context)