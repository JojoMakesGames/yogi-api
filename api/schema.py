import typing

import strawberry

from fastapi import FastAPI, Depends
from strawberry.fastapi import GraphQLRouter
from strawberry.types import Info

from database.session import get_session
from database import models as orm

from dataloaders import DataLoaders, DataLoadersExtension

from sqlalchemy import select

@strawberry.type
class ReviewSearchBrand:
    name: str

@strawberry.type
class ReviewSearchProduct:
    name: str
    views: typing.Optional[int]
    brand: ReviewSearchBrand

    @strawberry.field
    async def brand(self, info: Info) -> ReviewSearchBrand:
        return await info.context[DataLoaders.brands].load(self.brand)

@strawberry.type
class ReviewSearchReview:
    body: str
    rating: typing.Optional[int]
    product: ReviewSearchProduct

@strawberry.type
class Query:
    @strawberry.field
    async def brands(self, info: Info) -> typing.List[ReviewSearchBrand]:
        query = select(orm.Brand)
        async with info.context['session'] as session:
            brands = await session.execute(query)
        return brands.scalars().all()

    @strawberry.field
    async def products(self, info: Info) -> typing.List[ReviewSearchProduct]:
        query = select(orm.Product)
        async with info.context['session'] as session:
            products = (await session.scalars(query)).all()
        return products

async def get_context(
    session=Depends(get_session),
):
    return {
        "session": session,
    }



schema = strawberry.Schema(query=Query, extensions=[DataLoadersExtension])

graphql_app = GraphQLRouter(schema, context_getter=get_context)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")