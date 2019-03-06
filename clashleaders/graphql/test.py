import json
from collections import namedtuple

import graphene

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

    def resolve_things(self, info):
        print(info)
        return database


if __name__ == '__main__':
    schema = graphene.Schema(query=Query)
    result = schema.execute('{ things { status value  } }')
    print(json.dumps(result.data))
