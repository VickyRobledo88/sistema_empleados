CREATE DATABASE IF NOT EXISTS empleados;
USE empleados;

CREATE TABLE empleados (
    id INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(255),
    correo VARCHAR(255),
    foto VARCHAR(5000),
    PRIMARY KEY(id)
)

drop table empleado;

INSERT into empleados (nombre,correo,foto) VALUES('Mario','mario@email.com','fotodemario.jpg');
select * from empleados;