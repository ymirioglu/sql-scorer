SELECT customer_id,
       first_name,
       last_name
FROM   customers
WHERE  customer_id IN (
         SELECT  o.customer_id
         FROM    orders o
         GROUP BY o.customer_id
         HAVING  SUM(o.total_amount) >= 1000
       );