-----------
-- PESEL --
-----------
CREATE OR REPLACE FUNCTION validate_pesel(pesel TEXT)
RETURNS BOOLEAN AS
$$
DECLARE
    valid BOOLEAN := FALSE;
    pesel_length INTEGER;
    pesel_digits INTEGER[];
    weights INTEGER[] := '{1, 3, 7, 9, 1, 3, 7, 9, 1, 3, 1}';
    checksum INTEGER;
BEGIN
    pesel_length := length(pesel);

    -- Sprawdzenie długości numeru PESEL
    IF pesel_length = 11 THEN
        -- Sprawdzenie czy numer PESEL składa się z samych cyfr
        IF pesel ~ '^[0-9]+$' THEN
            pesel_digits := string_to_array(pesel, NULL);

            -- Obliczenie sumy kontrolnej
            checksum := (
                pesel_digits[1] * weights[1] +
                pesel_digits[2] * weights[2] +
                pesel_digits[3] * weights[3] +
                pesel_digits[4] * weights[4] +
                pesel_digits[5] * weights[5] +
                pesel_digits[6] * weights[6] +
                pesel_digits[7] * weights[7] +
                pesel_digits[8] * weights[8] +
                pesel_digits[9] * weights[9] +
                pesel_digits[10] * weights[10]
            ) % 10;

            -- Sprawdzenie sumy kontrolnej
            IF checksum = 0 THEN
                valid := (10 - pesel_digits[11]) = checksum;
            ELSE
                valid := (10 - checksum) = pesel_digits[11];
            END IF;
        END IF;
    END IF;
    IF valid = FALSE THEN
        RAISE EXCEPTION 'Invalid pesel!' USING ERRCODE = 'P0004';
    END IF;
    RETURN valid;
END;
$$
LANGUAGE plpgsql;

-------------
-- TELEFON --
-------------
CREATE OR REPLACE FUNCTION validate_phone_number(phone_number TEXT)
RETURNS BOOLEAN AS
$$
BEGIN
    -- Usunięcie spacji, myślników i innych znaków specjalnych z numeru telefonu
    phone_number := regexp_replace(phone_number, '[\s-]', '', 'g');

    -- Sprawdzenie, czy numer telefonu składa się z samych cyfr i ma odpowiednią długość
    IF phone_number ~ '^[+]?[0-9]+$' AND length(phone_number) >= 9 AND length(phone_number) <= 15 THEN
        RETURN TRUE;
    ELSE
        RAISE EXCEPTION 'Invalid phone number!' USING ERRCODE = 'P0003';
    END IF;
END;
$$
LANGUAGE plpgsql;


-----------
-- EMAIL --
-----------
CREATE OR REPLACE FUNCTION validate_email(email TEXT)
RETURNS BOOLEAN AS
$$
BEGIN
    -- Sprawdzenie ogólnego formatu adresu e-mail
    IF email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$' THEN
        RETURN TRUE;
    ELSE
        RAISE EXCEPTION 'Invalid email!' USING ERRCODE = 'P0002';
    END IF;
END;
$$
LANGUAGE plpgsql;


--------------------------
-- REJESTRACJA CZLOWIEK --
--------------------------
CREATE OR REPLACE FUNCTION validate_input_data_person(
    in_username TEXT,
    in_email TEXT,
    in_password TEXT,
    in_repeated_password TEXT,
    in_phone TEXT,
    in_pesel TEXT,
    in_first_name TEXT,
    in_second_name TEXT
)
RETURNS BOOLEAN AS
$$
DECLARE
    is_valid BOOLEAN := TRUE;
BEGIN
    -- Sprawdzenie poprawności nazwy użytkownika
    IF in_username IS NULL OR in_username = '' THEN
        is_valid := FALSE;
    END IF;

    -- Sprawdzenie poprawności imienia
    IF in_first_name IS NULL OR in_first_name = '' THEN
        is_valid := FALSE;
    END IF;

    -- Sprawdzenie poprawności nazwiska
    IF in_second_name IS NULL OR in_second_name = '' THEN
        is_valid := FALSE;
    END IF;

    -- Sprawdzenie poprawności adresu e-mail
    IF in_email IS NULL OR in_email = '' OR NOT validate_email(in_email) THEN
        is_valid := FALSE;
    END IF;

    -- Sprawdzenie poprawności hasła i powtórzonego hasła
    IF in_password IS NULL OR in_password = '' OR in_password <> in_repeated_password THEN
        is_valid := FALSE;
    END IF;

    -- Sprawdzenie poprawności numeru telefonu
    IF in_phone IS NULL OR in_phone = '' OR NOT validate_phone_number(in_phone) THEN
        is_valid := FALSE;
    END IF;

    -- Sprawdzenie poprawności numeru PESEL
    IF in_pesel IS NULL OR in_pesel = '' OR NOT validate_pesel(in_pesel) THEN
        is_valid := FALSE;
    END IF;
    IF is_valid = FALSE THEN
        RAISE EXCEPTION 'Invalid data!' USING ERRCODE = 'P0001';
    END IF;
    RETURN is_valid;
END;
$$
LANGUAGE plpgsql;


---------
-- NIP --
---------
CREATE OR REPLACE FUNCTION validate_nip(nip_input TEXT) RETURNS BOOLEAN AS
$$
DECLARE
  nip_pattern CONSTANT TEXT := '^\d{10}$';
  nip_sum INTEGER;
  i INTEGER;
BEGIN
  IF nip_input ~ nip_pattern THEN
    nip_sum := 0;

    FOR i IN 1..9 LOOP
      nip_sum := nip_sum + CAST(SUBSTRING(nip_input, i, 1) AS INTEGER) * (10 - i);
    END LOOP;

    nip_sum := nip_sum % 11;
    nip_sum := nip_sum % 10;

    RETURN nip_sum = CAST(SUBSTRING(nip_input, 10, 1) AS INTEGER);
  END IF;
    
  RETURN FALSE;
END;
$$
LANGUAGE plpgsql;



-----------------------
-- REJESTRACJA FIRMA --
-----------------------
CREATE OR REPLACE FUNCTION validate_input_data_company(
    in_username TEXT,
    in_email TEXT,
    in_password TEXT,
    in_repeated_password TEXT,
    in_phone TEXT,
    in_nip TEXT,
    in_name TEXT,
    in_sector TEXT
)
RETURNS BOOLEAN AS
$$
DECLARE
    is_valid BOOLEAN := TRUE;
BEGIN
    -- Sprawdzenie poprawności nazwy użytkownika
    IF in_username IS NULL OR in_username = '' THEN
        is_valid := FALSE;
    END IF;

    -- Sprawdzenie poprawności imienia
    IF in_name IS NULL OR in_name = '' THEN
        is_valid := FALSE;
    END IF;

    -- Sprawdzenie poprawności nazwiska
    IF in_sector IS NULL OR in_sector = '' THEN
        is_valid := FALSE;
    END IF;

    -- Sprawdzenie poprawności adresu e-mail
    IF in_email IS NULL OR in_email = '' OR NOT validate_email(in_email) THEN
        is_valid := FALSE;
    END IF;

    -- Sprawdzenie poprawności hasła i powtórzonego hasła
    IF in_password IS NULL OR in_password = '' OR in_password <> in_repeated_password THEN
        is_valid := FALSE;
    END IF;

    -- Sprawdzenie poprawności numeru telefonu
    IF in_phone IS NULL OR in_phone = '' OR NOT validate_phone_number(in_phone) THEN
        is_valid := FALSE;
    END IF;

    -- Sprawdzenie poprawności numeru NIP
    IF in_nip IS NULL OR in_nip = '' OR NOT validate_nip(in_nip) THEN
        is_valid := FALSE;
    END IF;

    RETURN is_valid;
END;
$$
LANGUAGE plpgsql;


----------------------------------
-- Sprawdzenie danych logowania --
----------------------------------
CREATE OR REPLACE FUNCTION check_login_form(
    login_param TEXT,
    haslo_param TEXT
    )
RETURNS BOOLEAN AS $$
DECLARE
    czy_istnieje BOOLEAN;
    poprawne_haslo BOOLEAN;
BEGIN
    -- Sprawdzenie, czy użytkownik istnieje
    SELECT TRUE INTO czy_istnieje FROM uzytkownicy WHERE login = login_param;

    IF czy_istnieje THEN
        -- Porównanie hasła
        SELECT (haslo = haslo_param) INTO poprawne_haslo FROM uzytkownicy WHERE login = login_param;
    END IF;

    RETURN poprawne_haslo;
END;
$$ LANGUAGE plpgsql;

---------------------------------
-- Empty Client record bug fix --
---------------------------------

CREATE OR REPLACE PROCEDURE fix_bug_client_empty_record()
AS $$
BEGIN
    UPDATE carrental_person SET client_ptr_id=parent_id WHERE client_ptr_id != parent_id;
    DELETE FROM carrental_client WHERE login='';
END;
$$ LANGUAGE plpgsql;