from django.db import models
from uuid import uuid4
from ..account.models import User
from ..product.models import Product

class Wishlist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    customer = models.ForeignKey(User, related_name="wishlists", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="wishlisted_by", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("customer", "product")
        ordering = ("-created_at",)

    def __str__(self):
        return f"Wishlist({self.customer}, {self.product})" 