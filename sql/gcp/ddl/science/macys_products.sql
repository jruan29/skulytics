CREATE TABLE `science-landing.landing.macys_products`
(
  url STRING,
  title STRING,
  brand STRING,
  reviews INT64,
  rating FLOAT64,
  description STRING,
  image STRING,
  productId STRING,
  category STRING,
  subcategory STRING,
  timestamp TIMESTAMP,
  skuId STRING,
  price FLOAT64,
  isOutOfStock BOOL,
  color STRING,
  isLowStock BOOL,
  productUnitSalesCount INT64,
  salePrice FLOAT64,
  socialBadges STRING
)
PARTITION BY DATE(timestamp)
CLUSTER BY productId;