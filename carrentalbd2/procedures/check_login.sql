DROP FUNCTION check_login(character varying,character varying);
CREATE OR REPLACE FUNCTION check_login(login_input varchar, password_input varchar)
  RETURNS boolean AS
$$
DECLARE
  valid_user boolean := false;
BEGIN
  -- Check if the login and password match in the carrental_client table
  SELECT true INTO valid_user
  FROM carrental_client
  WHERE (login = login_input AND password = password_input);

  RETURN valid_user;
END;
$$
LANGUAGE plpgsql;
