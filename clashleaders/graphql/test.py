import json
from collections import namedtuple

import graphene
from graphene.types.generic import GenericScalar

Row = namedtuple('Row', 'status value')

database = [
    Row(status='LIVE', value=1),  # value should be ignored and replaced with 12345
    Row(status='X', value=2),  # value should be preserved
]


class Something(graphene.ObjectType):
    status = graphene.String()
    value = graphene.Int()


class Query(graphene.ObjectType):
    things = graphene.List(Something)
    bar = graphene.List(graphene.List(GenericScalar))

    def resolve_bar(self, info):
        return [[1, "test", True], [1234, "test", True], [1, "test222", False]]

    @staticmethod
    def resolve_things(executor, info):
        return database


if __name__ == '__main__':
    schema = graphene.Schema(query=Query)
    result = schema.execute('{ bar }')
    print(json.dumps(result.data))
