-- Crear base de datos
CREATE DATABASE IF NOT EXISTS gestion_articulos;
USE gestion_articulos;

-- Crear tabla de artículos
CREATE TABLE IF NOT EXISTS articulos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(20) UNIQUE NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insertar datos de ejemplo
INSERT INTO articulos (codigo, descripcion, precio) VALUES
('ART001', 'Laptop HP Pavilion', 850.99),
('ART002', 'Mouse Inalámbrico Logitech', 25.50),
('ART003', 'Teclado Mecánico Redragon', 75.25),
('ART004', 'Monitor Samsung 24"', 299.99),
('ART005', 'Impresora Epson L380', 189.75);