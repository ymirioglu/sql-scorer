SELECT  c.customer_id,
        c.first_name,
        c.last_name
FROM    customers c
JOIN    orders o  ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
HAVING  SUM(o.total_amount) >= 1000;