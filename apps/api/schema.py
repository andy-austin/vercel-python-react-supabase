import strawberry


@strawberry.type
class Query:
    @strawberry.field
    def health(self) -> str:
        return "ok"


@strawberry.type
class Mutation:
    @strawberry.field
    def placeholder(self) -> str:
        return "No mutations defined yet"


schema = strawberry.Schema(query=Query, mutation=Mutation)
