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
        RETURN FALSE;
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
        RETURN FALSE;
    END IF;
END;
$$
LANGUAGE plpgsql;


-----------------
-- REJESTRACJA --
-----------------
CREATE OR REPLACE FUNCTION validate_input_data(
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

    RETURN is_valid;
END;
$$
LANGUAGE plpgsql;
