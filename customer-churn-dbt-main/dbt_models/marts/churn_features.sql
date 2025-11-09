-- Example: dbt_models/marts/churn_features.sql
SELECT
  c.customer_id,
  c.gender,
  c.contract_type,
  t.avg_monthly_spend,
  t.last_payment_date,
  DATE_PART('day', NOW() - t.last_payment_date) AS days_since_payment,
  CASE WHEN c.status = 'Inactive' THEN 1 ELSE 0 END AS churn_label
FROM raw.customers c
JOIN raw.transactions t USING(customer_id);
