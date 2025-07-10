import json
from django.core.management.base import BaseCommand
from django.test import Client
from django.conf import settings


class Command(BaseCommand):
    help = "Load sample products into the database via GraphQL"

    def handle(self, *args, **options):
        # Use Django's test client for internal requests
        client = Client()

        # GraphQL mutation
        mutation = """
        mutation ProductCreate($input: ProductCreateInput!) {
            productCreate(input: $input) {
                product {
                    id
                    name
                    slug
                }
                errors {
                    field
                    message
                    code
                }
            }
        }
        """

        # Sample data with corrected Python boolean values
        sample_data = [
            {
                "name": "UltraNote 14 Pro Laptop",
                "description": "The pinnacle of performance. A 14-inch powerhouse with the latest M3 Pro chip, 18GB unified memory, and a 512GB SSD. Perfect for creative professionals.",
                "category": "Q2F0ZWdvcnk6MQ==",
                "productType": "UHJvZHVjdFR5cGU6MQ==",
                "slug": "ultranote-14-pro-laptop-512gb",
                "seo": {
                    "title": "UltraNote 14 Pro Laptop | Professional Power",
                    "description": "Experience unparalleled speed with the UltraNote 14 Pro. Now available with an M3 Pro chip and 512GB of storage.",
                },
                "chargeTaxes": True,
                "taxCode": "PC010101",
                "weight": {"unit": "KG", "value": 1.6},
                "attributes": [
                    {"id": "QXR0cmlidXRlOjE=", "values": ["QXR0cmlidXRlVmFsdWU6MQ=="]},
                    {"id": "QXR0cmlidXRlOjI=", "values": ["QXR0cmlidXRlVmFsdWU6NQ=="]},
                ],
                "basePrice": {"amount": 1999.00, "currency": "USD"},
                "collections": ["Q29sbGVjdGlvbjoy"],
                "channelListings": [
                    {
                        "channelId": "Q2hhbm5lbDox",
                        "isPublished": True,
                        "publishedAt": "2024-03-15T09:00:00Z",
                        "visibleInListings": True,
                        "discountedPrice": None,
                    }
                ],
                "media": [
                    {
                        "alt": "Silver UltraNote 14 Pro Laptop",
                        "mediaUrl": "https://placehold.co/800x600/E2E8F0/4A5568?text=UltraNote+14",
                    }
                ],
                "translations": [],
                "trackInventory": True,
                "externalReference": "SKU-UN14P-512-SLV",
                "rating": 4.9,
            },
            {
                "name": "Aura Wireless Noise-Cancelling Headphones",
                "description": "Immerse yourself in sound. Industry-leading noise cancellation, 30-hour battery life, and crystal-clear call quality.",
                "category": "Q2F0ZWdvcnk6MQ==",
                "productType": "UHJvZHVjdFR5cGU6MQ==",
                "slug": "aura-wireless-headphones-black",
                "seo": {
                    "title": "Aura Noise-Cancelling Headphones",
                    "description": "Shop the Aura Wireless Headphones in Matte Black. Unrivaled sound and comfort.",
                },
                "chargeTaxes": True,
                "taxCode": "PC010102",
                "weight": {"unit": "G", "value": 254},
                "attributes": [
                    {"id": "QXR0cmlidXRlOjE=", "values": ["QXR0cmlidXRlVmFsdWU6Mg=="]}
                ],
                "basePrice": {"amount": 349.99, "currency": "USD"},
                "collections": ["Q29sbGVjdGlvbjoy", "Q29sbGVjdGlvbjoz"],
                "channelListings": [
                    {
                        "channelId": "Q2hhbm5lbDox",
                        "isPublished": True,
                        "publishedAt": "2024-01-20T09:00:00Z",
                        "visibleInListings": True,
                        "discountedPrice": {"amount": 299.99, "currency": "USD"},
                    }
                ],
                "media": [
                    {
                        "alt": "Matte Black Aura Headphones",
                        "mediaUrl": "https://placehold.co/800x800/1A202C/FFFFFF?text=Aura+Headphones",
                    }
                ],
                "translations": [],
                "trackInventory": True,
                "externalReference": "SKU-AWH-BLK",
                "rating": 4.7,
            },
            {
                "name": "Urban Explorer Tech Backpack",
                "description": "The perfect commuter bag. Water-resistant nylon, a padded 15-inch laptop sleeve, and multiple organizational pockets.",
                "category": "Q2F0ZWdvcnk6Mg==",
                "productType": "UHJvZHVjdFR5cGU6NA==",
                "slug": "urban-explorer-tech-backpack",
                "seo": {
                    "title": "Urban Explorer Tech Backpack | Commuter-Friendly",
                    "description": "Carry your tech safely and stylishly. Features a durable, water-resistant design.",
                },
                "chargeTaxes": True,
                "taxCode": "PC050101",
                "weight": {"unit": "KG", "value": 0.8},
                "attributes": [
                    {"id": "QXR0cmlidXRlOjE=", "values": ["QXR0cmlidXRlVmFsdWU6Mw=="]}
                ],
                "basePrice": {"amount": 89.95, "currency": "USD"},
                "collections": ["Q29sbGVjdGlvbjo0"],
                "channelListings": [
                    {
                        "channelId": "Q2hhbm5lbDox",
                        "isPublished": True,
                        "publishedAt": "2024-04-01T09:00:00Z",
                        "visibleInListings": True,
                        "discountedPrice": None,
                    }
                ],
                "media": [
                    {
                        "alt": "Charcoal Grey Tech Backpack",
                        "mediaUrl": "https://placehold.co/800x800/4A5568/FFFFFF?text=Backpack",
                    }
                ],
                "translations": [],
                "trackInventory": True,
                "externalReference": "SKU-UETB-CHR",
                "rating": 4.5,
            },
        ]

        successful_creates = 0
        failed_creates = 0

        self.stdout.write(f"Starting to load {len(sample_data)} products...")

        for i, product_data in enumerate(sample_data, 1):
            self.stdout.write(
                f"Creating product {i}/{len(sample_data)}: {product_data['name']}"
            )

            payload = {"query": mutation, "variables": {"input": product_data}}

            try:
                response = client.post(
                    "/graphql/",
                    data=json.dumps(payload),
                    content_type="application/json",
                )

                if response.status_code != 200:
                    self.stdout.write(
                        self.style.ERROR(
                            f"HTTP Error {response.status_code}: {response.content.decode()}"
                        )
                    )
                    failed_creates += 1
                    continue

                result = response.json()

                if "errors" in result:
                    self.stdout.write(
                        self.style.ERROR(f"GraphQL Error: {result['errors']}")
                    )
                    failed_creates += 1
                elif result["data"]["productCreate"]["errors"]:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Product Creation Error: {result['data']['productCreate']['errors']}"
                        )
                    )
                    failed_creates += 1
                else:
                    product = result["data"]["productCreate"]["product"]
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Successfully created: {product['name']} (ID: {product['id']})"
                        )
                    )
                    successful_creates += 1

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Request failed: {str(e)}"))
                failed_creates += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Completed: {successful_creates} successful, {failed_creates} failed"
            )
        )
