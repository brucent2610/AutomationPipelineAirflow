CREATE OR REPLACE TABLE `{{ params.staging_dataset }}.D_TIKI` AS
SELECT 
  *,
  REGEXP_REPLACE(
    REGEXP_REPLACE(
      REGEXP_REPLACE(
        REGEXP_REPLACE(
          REGEXP_REPLACE(
            LOWER(description),
            r"<br>|<br\/>|<br\s+\/>|<\/p>", "\n"),
          r"<[^>]*>", ""),
        r"\n{2,}", "\n\n"),
      r"^\s+", ""),
    r"\n\s+", "\n") as description,
    price * quantity_sold.value as total,
    case
        when inventory_status = "available" then "yes"
        else "no"
    end as in_stock,
    DATE_ADD(CURRENT_DATE(), INTERVAL -day_ago_created DAY) AS created_at,
    categories.id as cat_id
FROM `{{ params.project_id }}.{{ params.staging_dataset }}.{{ params.table }}` 
WHERE inventory_status = "available"