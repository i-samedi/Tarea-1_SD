-- Car_Name;Year;Selling_Price;Present_Price;Kms_Driven;Fuel_Type;Seller_Type;Transmission;Owner
-- crea la base de datos
CREATE DATABASE cars;
-- conecta a la base de datos
\c cars;
-- crea la tabla
CREATE TABLE cars (
    id BIGINT PRIMARY KEY not null,
    car_name VARCHAR(100),
    car_year INTEGER,
    Selling_Price FLOAT,
    Present_Price FLOAT,
    Kms_Driven INTEGER,
    Fuel_Type VARCHAR(100),
    Seller_Type VARCHAR(100),
    Transmission VARCHAR(100),
    Owner INTEGER
);

COPY cars 
FROM '/Users/lordsamedi/Desktop/myFolder/Universidad/7to/Tarea_1_SD/data/cardata 2.csv' 
DELIMITER ';' 
CSV HEADER;

-- CREATE ROLE tiago WITH LOGIN PASSWORD 'tarea11';
-- GRANT ALL PRIVILEGES ON DATABASE tarea1 TO tiago;

