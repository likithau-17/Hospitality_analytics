USE hospitality_analytics;

CREATE TABLE dim_hotel (
    hotel_id CHAR(36) PRIMARY KEY,
    hotel_name VARCHAR(100),
    location VARCHAR(100),
    hotel_type VARCHAR(50),
    room_capacity INT
);

CREATE TABLE dim_room (
    room_id CHAR(36) PRIMARY KEY,
    hotel_id CHAR(36),
    room_type VARCHAR(50),
    room_number VARCHAR(20),
    FOREIGN KEY (hotel_id) REFERENCES dim_hotel(hotel_id)
);

CREATE TABLE dim_guest (
    guest_id CHAR(36) PRIMARY KEY,
    guest_name VARCHAR(100),
    guest_type VARCHAR(50),
    country VARCHAR(50)
);

CREATE TABLE dim_employee (
    employee_id CHAR(36) PRIMARY KEY,
    employee_name VARCHAR(100),
    position VARCHAR(50),
    department VARCHAR(50),
    hotel_id CHAR(36),
    FOREIGN KEY (hotel_id) REFERENCES dim_hotel(hotel_id)
);

CREATE TABLE dim_date (
    date_id INT PRIMARY KEY,
    full_date DATE,
    day INT,
    month INT,
    month_name VARCHAR(20),
    quarter INT,
    year INT,
    season VARCHAR(30)
);

-- 1. Room Night Fact
CREATE TABLE fact_room_night (
    room_night_id CHAR(36) PRIMARY KEY,
    hotel_id CHAR(36),
    room_id CHAR(36),
    date_id INT,
    is_available TINYINT,
    is_occupied TINYINT,
    room_revenue DECIMAL(12,2),

    FOREIGN KEY (hotel_id) REFERENCES dim_hotel(hotel_id),
    FOREIGN KEY (room_id) REFERENCES dim_room(room_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);

-- 2. Guest Feedback Fact
CREATE TABLE fact_guest_feedback (
    feedback_id CHAR(36) PRIMARY KEY,
    guest_id CHAR(36),
    hotel_id CHAR(36),
    date_id INT,
    satisfaction_rating DECIMAL(2,1),

    FOREIGN KEY (guest_id) REFERENCES dim_guest(guest_id),
    FOREIGN KEY (hotel_id) REFERENCES dim_hotel(hotel_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);

-- 3. Employee Movement Fact
CREATE TABLE fact_employee_movement (
    movement_id CHAR(36) PRIMARY KEY,
    employee_id CHAR(36),
    hotel_id CHAR(36),
    date_id INT,
    movement_type VARCHAR(10),

    FOREIGN KEY (employee_id) REFERENCES dim_employee(employee_id),
    FOREIGN KEY (hotel_id) REFERENCES dim_hotel(hotel_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);