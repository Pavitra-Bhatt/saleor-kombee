from ...wishlist.models import Wishlist
from ..core.context import get_database_connection_name
from ..utils import get_user_or_app_from_context


def resolve_wishlist_items(info):
    user = get_user_or_app_from_context(info.context)
    if not user or not user.is_authenticated:
        return Wishlist.objects.none()

    database_connection_name = get_database_connection_name(info.context)
    qs = (
        Wishlist.objects.using(database_connection_name)
        .filter(customer=user)
        .select_related("product")
    )
    for w in qs:
        product = w.product
    return qs
