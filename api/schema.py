import typing
import strawberry

@strawberry.type
class Brand:
    name: str

@strawberry.type
class Query:
    brands: typing.List[Brand]


def get_books():
    return [
        Brand(
            name='Workds',
        ),
    ]

@strawberry.type
class Query:
    books: typing.List[Brand] = strawberry.field(resolver=get_books) 


schema = strawberry.Schema(query=Query)