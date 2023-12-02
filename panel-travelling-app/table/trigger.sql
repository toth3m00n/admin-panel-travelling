CREATE OR REPLACE FUNCTION count_bill_for_booking()
    RETURNS trigger AS
$$
BEGIN
    room_class = SELECT class_name FROM room WHERE number=room_number;
    class_price = SELECT price FROM class WHERE name=room_class;
    NEW.price = ROUND(EXTRACT(hours from (NEW.session_end - NEW.session_start)), 1) * class_price;
    RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE OR REPLACE TRIGGER set_booking_price
    BEFORE INSERT ON booking
    FOR EACH ROW
    EXECUTE FUNCTION count_bill_for_booking();