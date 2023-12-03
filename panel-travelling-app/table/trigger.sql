CREATE OR REPLACE FUNCTION count_bill_for_booking()
    RETURNS trigger AS
$$
DECLARE
    class_price NUMERIC (10, 1);
BEGIN
    SELECT price_per_night FROM class INTO class_price WHERE NEW.class_id=id;
    NEW.price = ROUND(EXTRACT(days from (NEW.check_out - NEW.check_in)), 1) * class_price;
    RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE OR REPLACE TRIGGER set_booking_price
    BEFORE INSERT ON booking
    FOR EACH ROW
    EXECUTE FUNCTION count_bill_for_booking();