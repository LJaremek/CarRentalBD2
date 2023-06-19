SELECT m.name, c.plate, r.id, r.start_date, r.end_date
FROM carrental_client k
JOIN carrental_rental r ON r.client_id_id = k.id
JOIN carrental_car c ON r.car_id_id = c.id
JOIN carrental_carmodel m ON m.id = c.car_model_id
WHERE k.id = %s AND r.end_date IS NOT NULL
ORDER BY r.end_date DESC;