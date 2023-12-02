CREATE OR REPLACE FUNCTION count_bill_for_booking()
    RETURNS trigger AS
$$
DECLARE
    room_class INT;
    class_price NUMERIC (6, 1);
BEGIN
    SELECT class_name INTO room_class FROM room WHERE number=room_number;
    SELECT price FROM class INTO class_price WHERE name=room_class;
    NEW.price = ROUND(EXTRACT(hours from (NEW.check_out - NEW.check_in)), 1) * class_price;
    RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE OR REPLACE TRIGGER set_booking_price
    BEFORE INSERT ON booking
    FOR EACH ROW
    EXECUTE FUNCTION count_bill_for_booking();