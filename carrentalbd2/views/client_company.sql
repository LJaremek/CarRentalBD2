SELECT c.country, c.email, c.login, c.phone, k.name, k.nip, k.sector, c.id
FROM carrental_client c JOIN carrental_company k ON c.id = k.parent_id
WHERE c.login = %s;