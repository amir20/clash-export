import logging

import graphene

from clashleaders.views import imgproxy_url

logger = logging.getLogger(__name__)


class BadgeUrls(graphene.ObjectType):
    large = graphene.String()
    medium = graphene.String()
    small = graphene.String()
    tiny = graphene.String()

    def resolve_large(self, info):
        return imgproxy_url(self.large)

    def resolve_medium(self, info):
        return imgproxy_url(self.medium)

    def resolve_small(self, info):
        return imgproxy_url(self.small)

    def resolve_tiny(self, info):
        return imgproxy_url(self.tiny)
