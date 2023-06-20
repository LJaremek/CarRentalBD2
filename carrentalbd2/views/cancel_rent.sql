UPDATE carrental_rental
SET rental_status = 'finished', end_date = CURRENT_TIMESTAMP WHERE
id = %s;
