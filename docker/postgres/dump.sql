CREATE TABLE products (
  code VARCHAR(10) NOT NULL,
  unit_price DECIMAL(10, 2) NOT NULL,
  special_price VARCHAR(20)
);

INSERT INTO products (unit_price, special_price, code)
VALUES
(50, '3 for 140', 'A'),
(35, '2 for 60', 'B'),
(25, NULL, 'C'),
(12, NULL, 'D');