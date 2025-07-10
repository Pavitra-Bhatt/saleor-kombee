import graphene
from ...permission.auth_filters import AuthorizationFilters
from ..core.fields import BaseField, FilterConnectionField
from ..core.types import NonNullList
from .types import WishlistType, WishlistCountableConnection
from .resolvers import resolve_wishlist_items
from ..core import ResolveInfo
from ..core.doc_category import DOC_CATEGORY_PRODUCTS
from .mutations import AddToWishlist, RemoveFromWishlist
from ..channel.dataloaders import ChannelBySlugLoader

from ..core.connection import filter_connection_queryset, create_connection_slice


class WishlistQueries(graphene.ObjectType):
    wishlist_items = FilterConnectionField(
        WishlistCountableConnection,
        description="List of the current user's wishlist items.",
        doc_category=DOC_CATEGORY_PRODUCTS,
    )

    @staticmethod
    def resolve_wishlist_items(_root, info: ResolveInfo, *, channel=None, **kwargs):
        user = info.context.user
        if not user or not user.is_authenticated:
            from ...wishlist.models import Wishlist
            return Wishlist.objects.none()
        limited_channel_access = False if channel is None else True

        def _resolve_wishlist_items(channel_obj):
            qs = resolve_wishlist_items(info)
            # Optionally, filter by channel if your wishlist is channel-specific
            kwargs["channel"] = channel
            qs = filter_connection_queryset(
                qs, kwargs, allow_replica=info.context.allow_replica
            )
            return create_connection_slice(qs, info, kwargs, WishlistCountableConnection)

        if channel:
            return (
                ChannelBySlugLoader(info.context)
                .load(str(channel))
                .then(_resolve_wishlist_items)
            )
        return _resolve_wishlist_items(None)


class Query(WishlistQueries, graphene.ObjectType):
    pass


class Mutation(graphene.ObjectType):
    add_to_wishlist = AddToWishlist.Field()
    remove_from_wishlist = RemoveFromWishlist.Field() 