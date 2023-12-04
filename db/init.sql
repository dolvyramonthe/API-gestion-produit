
-- Table product
DROP DATABASE IF EXISTS API;
CREATE DATABASE API;
USE API;

CREATE TABLE IF NOT EXISTS products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    image_path VARCHAR(255),
    status VARCHAR(50) DEFAULT 'Disponible' NOT NULL
);

-- Table users
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('USER', 'ADMIN') NOT NULL DEFAULT 'USER'
);

-- Table roles
CREATE TABLE IF NOT EXISTS roles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL
);

-- Table  JWT tokens 
CREATE TABLE IF NOT EXISTS tokens (
    user_id INT,
    token VARCHAR(1024),
    expiration_date DATETIME
);

-- Table carts
CREATE TABLE IF NOT EXISTS carts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    product_id INT,
    quantity INT NOT NULL DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);



INSERT INTO users (username, email, password, role) VALUES ('admin', 'monthe@etna.com ', 'motdepasseadmin', 'ADMIN');

INSERT INTO users (username, email, password, role) VALUES ('user', 'rose@etna.com ', 'motdepasseadmin', 'ADMIN');
