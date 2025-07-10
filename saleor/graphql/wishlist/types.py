import graphene
from ...wishlist import models
from ..core.connection import CountableConnection
from ..core.types import ModelObjectType
from ..product.types import Product
from ..channel import ChannelContext


class WishlistType(ModelObjectType):
    id = graphene.GlobalID(required=True)
    product = graphene.Field(Product, required=False, description="The product being wishlisted.")

    class Meta:
        description = "Represents a wishlist item."
        interfaces = [graphene.relay.Node]
        model = models.Wishlist

    def resolve_product(self, info):
        product = getattr(self, "product", None)
        if not product:
            return None
        if not isinstance(product, ChannelContext):
            return ChannelContext(node=product, channel_slug=None)
        return product

class WishlistCountableConnection(CountableConnection):
    class Meta:
        node = WishlistType