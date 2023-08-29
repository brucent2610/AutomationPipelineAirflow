CREATE OR REPLACE TABLE `{{ params.staging_dataset }}.R_TIKI` AS
SELECT
  p.id as id,
  p.sku as sku,
  p.name as name,
  REGEXP_REPLACE(
    REGEXP_REPLACE(
      REGEXP_REPLACE(
        REGEXP_REPLACE(
          REGEXP_REPLACE(
            LOWER(p.description),
            r"<br>|<br\/>|<br\s+\/>|<\/p>", "\n"),
          r"<[^>]*>", ""),
        r"\n{2,}", "\n\n"),
      r"^\s+", ""),
    r"\n\s+", "\n") as description,
    p.price as price,
    p.quantity_sold.value as selling_count,
    p.price * p.quantity_sold.value as total,
    case
        when p.inventory_status = "available" then "yes"
        else "no"
    end as in_stock,
    DATE_ADD(CURRENT_DATE(), INTERVAL -p.day_ago_created DAY) AS created_at,
    p.categories.id as cat_id,
    p.categories.name as cat_name,
    p.rating_average as rating,
    p.current_seller.id as seller_id,
    p.current_seller.name as seller_name,
    (
      SELECT (
        SELECT value
        FROM UNNEST(specs.attributes)
        WHERE code = "brand_country"
        LIMIT 1
      ) AS brand_country
      FROM UNNEST(p.specifications) as specs
      LIMIT 1
    ) AS made_in
FROM `{{ params.project_id }}.{{ params.staging_dataset }}.{{ params.table }}` as p
WHERE p.inventory_status = "available"