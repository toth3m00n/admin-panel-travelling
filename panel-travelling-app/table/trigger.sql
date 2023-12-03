CREATE OR REPLACE FUNCTION count_bill_for_booking()
    RETURNS trigger AS
$$
DECLARE
    class_price NUMERIC (6, 1);
BEGIN
    SELECT price FROM class INTO class_price WHERE NEW.class_name=name AND NEW.hotel_name=hotel_name;
    NEW.price = ROUND(EXTRACT(hours from (NEW.check_out - NEW.check_in)), 1) * class_price;
    RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE OR REPLACE TRIGGER set_booking_price
    BEFORE INSERT ON booking
    FOR EACH ROW
    EXECUTE FUNCTION count_bill_for_booking();