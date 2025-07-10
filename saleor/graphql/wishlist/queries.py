import graphene
from .types import WishlistType
from saleor.wishlist.models import Wishlist

class Query(graphene.ObjectType):
    my_wishlist = graphene.List(WishlistType, description="Current user's wishlist items.")

    def resolve_my_wishlist(self, info):
        user = info.context.user
        if not user or not user.is_authenticated:
            return []
        return Wishlist.objects.filter(customer=user).select_related("product") 