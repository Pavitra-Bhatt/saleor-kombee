#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'saleor.settings')
django.setup()

from saleor.shipping.models import ShippingZone, ShippingMethod, ShippingMethodChannelListing
from saleor.channel.models import Channel
from saleor.warehouse.models import Country
from decimal import Decimal

def setup_shipping_methods():
    print("=== Setting up Shipping Methods ===\n")

    # Get the online-inr channel
    try:
        channel = Channel.objects.get(id=3)  # online-inr channel
        print(f"Target channel: {channel.name} ({channel.slug})")
    except Channel.DoesNotExist:
        print("Channel with ID 3 not found. Available channels:")
        for ch in Channel.objects.all():
            print(f"  - {ch.name} (ID: {ch.id}, Slug: {ch.slug})")
        return

    # Check existing shipping zones
    shipping_zones = ShippingZone.objects.all()
    print(f"\nExisting shipping zones: {shipping_zones.count()}")

    # Create shipping zone for India if it doesn't exist
    india_zone = None
    for zone in shipping_zones:
        if "india" in zone.name.lower() or "IN" in [c.code for c in zone.countries.all()]:
            india_zone = zone
            print(f"Found existing India zone: {zone.name}")
            break

    if not india_zone:
        print("Creating new shipping zone for India...")
        india_zone = ShippingZone.objects.create(
            name="India",
            default=False
        )

        # Add India to the zone
        try:
            india_country = Country.objects.get(code="IN")
            india_zone.countries.add(india_country)
            print(f"Added India (IN) to shipping zone")
        except Country.DoesNotExist:
            print("Warning: Country 'IN' not found in database")

    # Check existing shipping methods
    existing_methods = ShippingMethod.objects.filter(shipping_zone=india_zone)
    print(f"\nExisting shipping methods in {india_zone.name}: {existing_methods.count()}")

    # Create shipping methods if they don't exist
    shipping_methods = []

    # Standard Shipping
    standard_method, created = ShippingMethod.objects.get_or_create(
        name="Standard Shipping",
        shipping_zone=india_zone,
        defaults={
            'price_amount': Decimal('100.00'),
            'minimum_order_price_amount': Decimal('0.00'),
            'maximum_order_price_amount': None,
            'type': 'price'
        }
    )
    shipping_methods.append(standard_method)
    if created:
        print(f"Created: {standard_method.name} - ₹{standard_method.price_amount}")
    else:
        print(f"Found existing: {standard_method.name} - ₹{standard_method.price_amount}")

    # Express Shipping
    express_method, created = ShippingMethod.objects.get_or_create(
        name="Express Shipping",
        shipping_zone=india_zone,
        defaults={
            'price_amount': Decimal('250.00'),
            'minimum_order_price_amount': Decimal('0.00'),
            'maximum_order_price_amount': None,
            'type': 'price'
        }
    )
    shipping_methods.append(express_method)
    if created:
        print(f"Created: {express_method.name} - ₹{express_method.price_amount}")
    else:
        print(f"Found existing: {express_method.name} - ₹{express_method.price_amount}")

    # Free Shipping for orders over ₹1000
    free_method, created = ShippingMethod.objects.get_or_create(
        name="Free Shipping",
        shipping_zone=india_zone,
        defaults={
            'price_amount': Decimal('0.00'),
            'minimum_order_price_amount': Decimal('1000.00'),
            'maximum_order_price_amount': None,
            'type': 'price'
        }
    )
    shipping_methods.append(free_method)
    if created:
        print(f"Created: {free_method.name} - ₹{free_method.price_amount} (min order: ₹{free_method.minimum_order_price_amount})")
    else:
        print(f"Found existing: {free_method.name} - ₹{free_method.price_amount}")

    # Add shipping methods to the channel
    print(f"\n=== Adding shipping methods to channel: {channel.name} ===")

    for method in shipping_methods:
        # Check if channel listing already exists
        listing, created = ShippingMethodChannelListing.objects.get_or_create(
            shipping_method=method,
            channel=channel,
            defaults={
                'price_amount': method.price_amount,
                'minimum_order_price_amount': method.minimum_order_price_amount or Decimal('0.00'),
                'maximum_order_price_amount': method.maximum_order_price_amount
            }
        )

        if created:
            print(f"Added to channel: {method.name} - ₹{listing.price_amount}")
        else:
            print(f"Already exists in channel: {method.name} - ₹{listing.price_amount}")

    # Verify the setup
    print(f"\n=== Verification ===")
    available_methods = ShippingMethodChannelListing.objects.filter(channel=channel)
    print(f"Total shipping methods available in {channel.name}: {available_methods.count()}")

    for listing in available_methods:
        method = listing.shipping_method
        print(f"  - {method.name}: ₹{listing.price_amount}")
        if method.minimum_order_price_amount > 0:
            print(f"    (Minimum order: ₹{method.minimum_order_price_amount})")

    print(f"\n=== Setup Complete ===")
    print("You can now use these shipping method IDs in your checkout mutations:")
    for listing in available_methods:
        method = listing.shipping_method
        # Generate the Relay Global ID
        from saleor.core.utils import generate_unique_slug
        import base64
        method_id = base64.b64encode(f"ShippingMethod:{method.id}".encode()).decode()
        print(f"  - {method.name}: {method_id}")

if __name__ == "__main__":
    setup_shipping_methods()
