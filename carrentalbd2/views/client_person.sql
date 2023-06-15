SELECT c.country, c.email, c.login, c.phone, p.first_name, p.pesel, p.second_name, c.id
FROM carrental_client c JOIN carrental_person p ON c.id = p.parent_id
WHERE c.login = %s;