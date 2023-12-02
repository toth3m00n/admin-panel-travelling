CREATE TABLE IF NOT EXISTS client (
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 ),
    booking_id INT REFERENCES booking (id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    sex CHAR NOT NULL,
    age INT NOT NULL,
    room INT NOT NULL,
    telephone TEXT,
    job TEXT,
    CONSTRAINT valid_room CHECK (room > 0),
    CONSTRAINT valid_age CHECK (age > 0 AND age < 130),
    CONSTRAINT valid_sex CHECK (sex = 'male' or sex = 'female')
);

CREATE TABLE IF NOT EXIST convenience (
    name TEXT PRIMARY KEY
);

CREATE TABLE IF NOT EXIST class (
    name TEXT PRIMARY KEY,
    price_per_night NUMERIC (6, 1) NOT NULL
);

CREATE TABLE IF NOT EXIST class-convenience (
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY (INCREMENT 1, START 1),
    convenience_name TEXT REFERENCES convenience (name) ON DELETE CASCADE,
    class_name TEXT REFERENCES class (name) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXIST hotel (
    name TEXT PRIMARY KEY,
    count_stars NUMERIC(2, 1) NOT NULL
);

CREATE TABLE IF NOT EXIST room (
    number INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY (INCREMENT 1, START 1),
    class_name TEXT REFERENCES class (name) ON DELETE CASCADE,
    hotel_name TEXT REFERENCES hotel (name) ON DELETE CASCADE,
    number_seats INT NOT NULL,
    CONSTRAINT valid_number_seats CHECK (number_seats > 0)
);


CREATE TABLE IF NOT EXIST booking (
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 ),
    room_number INT REFERENCES room (number) ON DELETE CASCADE,
    check_in TIMESTAMP WITH TIME ZONE,
    check_out TIMESTAMP WITH TIME ZONE,
    price NUMERIC(7, 1),
    CONSTRAINT valid_session_time CHECK (check_in < check_out)
);


