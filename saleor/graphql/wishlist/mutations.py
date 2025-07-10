import graphene
from django.core.exceptions import ValidationError
from ...core.exceptions import PermissionDenied
from ...wishlist import models
from ...wishlist.error_codes import WishlistErrorCode
from ..core import ResolveInfo
from ..core.mutations import BaseMutation
from ..product.types import Product
from .types import WishlistType
from ..utils import get_user_or_app_from_context
from ..channel import ChannelContext

# Define the Graphene Enum from the Python Enum
WishlistErrorCodeEnum = graphene.Enum.from_enum(WishlistErrorCode)

class WishlistErrorType(graphene.ObjectType):
    field = graphene.String(
        description=(
            "Name of a field that caused the error. A value of `null` indicates that "
            "the error isn't associated with a particular field."
        ),
        required=False,
    )
    message = graphene.String(description="The error message.", required=False)
    code = WishlistErrorCodeEnum(description="The error code.", required=True)

    def resolve_product(self, info):
        # If the product is not wrapped, wrap it in a ChannelContext with no channel
        from ..channel import ChannelContext
        product = self.product
        if not isinstance(product, ChannelContext):
            return ChannelContext(node=product, channel_slug=None)
        return product


class WishlistBaseMutation(BaseMutation):
    class Meta:
        abstract = True

    @classmethod
    def _check_permissions(cls, context):
        if not context.user.is_authenticated:
            raise PermissionDenied(message="Authentication required.")
        return context.user


class AddToWishlist(WishlistBaseMutation):
    wishlist = graphene.Field(
        WishlistType, description="The wishlist entry that was created."
    )

    class Arguments:
        product_id = graphene.ID(required=True, description="ID of the product to add.")

    class Meta:
        description = "Adds a product to the user's wishlist."
        error_type_class = WishlistErrorType

    @classmethod
    def perform_mutation(cls, _root, info: ResolveInfo, /, **data):
        user = cls._check_permissions(info.context)
        product_id = data["product_id"]

        try:
            product = cls.get_node_or_error(
                info, product_id, field="product_id", only_type=Product
            )
        except ValidationError as error:
            return cls.handle_errors(error)

        wishlist, _created = models.Wishlist.objects.get_or_create(
            customer=user, product=product
        )
        return AddToWishlist(wishlist=wishlist)


class RemoveFromWishlist(graphene.Mutation):
    class Arguments:
        wishlist_id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, wishlist_id):
        user = info.context.user
        if not user or not user.is_authenticated:
            return RemoveFromWishlist(ok=False)
        from graphene import Node
        _type, db_id = Node.from_global_id(wishlist_id)
        deleted, _ = models.Wishlist.objects.filter(id=db_id, customer=user).delete()
        return RemoveFromWishlist(ok=deleted > 0)