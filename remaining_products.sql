-- =====================================================
-- REMAINING PRODUCTS (fixing duplicate external references)
-- =====================================================

-- Product 21: Women's All-Weather Running Jacket (Coral) - Fixed external reference
INSERT INTO product_product (
    id, name, description, updated_at, product_type_id, category_id,
    seo_description, seo_title, weight, metadata, private_metadata,
    slug, description_plaintext, rating,
    search_document, created_at, search_vector, search_index_dirty,
    tax_class_id, external_reference
) VALUES (
    26, 'Women''s All-Weather Running Jacket (Coral)',
    '{"blocks": [{"data": {"text": "Don''t let the weather stop you. A lightweight, wind-resistant, and water-repellent jacket with reflective details for visibility."}, "type": "paragraph"}]}',
    '2024-01-01 10:00:00+00', 25, 47,
    'Stay protected on your run with our breathable and stylish all-weather jacket.', 'Women''s All-Weather Running Jacket',
    0.28, '{}', '{}', 'womens-all-weather-running-jacket-coral-v2',
    'Don''t let the weather stop you. A lightweight, wind-resistant, and water-repellent jacket with reflective details for visibility.',
    4.7, 'womens all weather running jacket coral wind resistant water repellent',
    '2024-01-01 10:00:00+00', NULL, false, 3, 'SKU-WARJ-CRL-S-V2'
);

-- =====================================================
-- PRODUCT CHANNEL LISTINGS
-- =====================================================

-- Channel listing for the remaining product
INSERT INTO product_productchannellisting (
    product_id, channel_id, is_published, published_at,
    visible_in_listings, available_for_purchase_at,
    discounted_price_amount, currency, discounted_price_dirty
) VALUES
(26, 3, true, '2024-05-01 09:00:00+00', true, '2024-05-01 09:00:00+00', 110.00, 'INR', false);

-- =====================================================
-- PRODUCT MEDIA
-- =====================================================

-- Product media for the remaining product
INSERT INTO product_productmedia (
    product_id, alt, type, oembed_data, to_remove, metadata, private_metadata
) VALUES
(26, 'Coral running jacket', 'IMAGE', '{}', false, '{}', '{}');

-- =====================================================
-- UPDATE SEQUENCES
-- =====================================================

-- Update sequences to ensure proper auto-increment
SELECT setval('product_product_id_seq', (SELECT MAX(id) FROM product_product));
SELECT setval('product_productchannellisting_id_seq', (SELECT MAX(id) FROM product_productchannellisting));
SELECT setval('product_productmedia_id_seq', (SELECT MAX(id) FROM product_productmedia));

-- =====================================================
-- END OF REMAINING DATA
-- =====================================================
