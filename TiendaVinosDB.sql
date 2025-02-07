DROP DATABASE IF EXISTS TiendaVinosDB;
CREATE DATABASE IF NOT EXISTS TiendaVinosDB;

USE TiendaVinosDB;

DROP TABLE IF EXISTS vinos;
CREATE TABLE IF NOT EXISTS vinos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10, 2) NOT NULL,
    categoria VARCHAR(255),
    imagen VARCHAR(255),
    stock INT NOT NULL
);

DROP TABLE IF EXISTS usuarios;
CREATE TABLE IF NOT EXISTS usuarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);

DROP TABLE IF EXISTS pedidos;
CREATE TABLE IF NOT EXISTS pedidos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

DROP TABLE IF EXISTS items_pedido;
CREATE TABLE IF NOT EXISTS items_pedido (
    id INT PRIMARY KEY AUTO_INCREMENT,
    pedido_id INT NOT NULL,
    vino_id INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
    FOREIGN KEY (vino_id) REFERENCES vinos(id)
);


CREATE VIEW vinos_tintos AS
SELECT
    id,
    nombre,
    descripcion,
    precio,
    categoria,
    imagen,
    stock
FROM
    vinos
WHERE
    categoria = 'Tinto';

CREATE VIEW vinos_blancos AS
SELECT
    id,
    nombre,
    descripcion,
    precio,
    categoria,
    imagen,
    stock
FROM
    vinos
WHERE
    categoria = 'Blanco';
    
    
CREATE VIEW pedidos_detallados AS
SELECT
    p.id AS pedido_id,
    p.fecha,
    p.total,
    u.username AS usuario,
    i.cantidad,
    i.precio_unitario,
    v.nombre AS vino
FROM
    pedidos p
INNER JOIN
    usuarios u ON p.usuario_id = u.id
INNER JOIN
    items_pedido i ON p.id = i.pedido_id
INNER JOIN
    vinos v ON i.vino_id = v.id;
    
CREATE VIEW ventas_por_vino AS
SELECT
    v.id AS vino_id,
    v.nombre AS vino,
    SUM(i.cantidad) AS cantidad_vendida
FROM
    vinos v
LEFT JOIN
    items_pedido i ON v.id = i.vino_id
GROUP BY
    v.id, v.nombre;

INSERT INTO usuarios (username, password, is_admin) VALUES ('admin', 'admin', TRUE);