-- Display car information
CREATE OR REPLACE VIEW car_info_view AS
SELECT c.car_status, m.name, m.seats_number, m.doors_number, m.produced_date
FROM carrental_car c
JOIN carrental_carmodel m ON c.car_model_id = m.id;