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
    foo = graphene.String()

    def resolve_foo(self, info):
        return "hi there!" + self.status


class Query(graphene.ObjectType):
    things = graphene.List(Something)

    @staticmethod
    def resolve_things(executor, info):
        return database


if __name__ == '__main__':
    schema = graphene.Schema(query=Query)
    result = schema.execute('{ things { status value foo } }')
    print(json.dumps(result.data))  # {"things": [{"status": "LIVE", "value": 12345}, {"status": "X", "value": 12345}]}
