CREATE OR REPLACE PROCEDURE remove_duplicate AS
BEGIN
  -- Update query
  UPDATE carrental_person
  SET client_ptr_id=parent_id
  WHERE client_ptr_id!=parent_id;
  
  -- Delete query
  DELETE FROM carrental_client
  WHERE login = '';
  
  -- Commit the changes
  COMMIT;
END;


