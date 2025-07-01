-- Script de inicialización para Docker
CREATE DATABASE IF NOT EXISTS pacientes_monitoreo;
USE pacientes_monitoreo;

CREATE TABLE IF NOT EXISTS `pacientes` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `nombre` VARCHAR(100) NOT NULL,
  `edad` INT NOT NULL,
  `genero` ENUM('M','F') NOT NULL,
  `activo` BOOLEAN DEFAULT true
);

CREATE TABLE IF NOT EXISTS `mediciones` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `id_paciente` INT NOT NULL,
  `timestamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `spo2` DECIMAL(5,2) NOT NULL,
  `bpm` INT NOT NULL,
  `temperatura` DECIMAL(4,2) NOT NULL,
  FOREIGN KEY (`id_paciente`) REFERENCES `pacientes` (`id`)
);

CREATE TABLE IF NOT EXISTS `alertas` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `id_paciente` INT NOT NULL,
  `tipo` ENUM('verde','amarilla','roja') NOT NULL,
  `mensaje` VARCHAR(255) NOT NULL,
  `timestamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`id_paciente`) REFERENCES `pacientes` (`id`)
);

CREATE TABLE IF NOT EXISTS `predicciones` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `id_paciente` INT NOT NULL,
  `enfermedad` VARCHAR(100) NOT NULL,
  `probabilidad` DECIMAL(5,4) NOT NULL,
  `timestamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `id_paciente` INT NOT NULL,
  FOREIGN KEY (`id_paciente`) REFERENCES `pacientes` (`id`)
);

-- Crear usuario para la aplicación
CREATE USER IF NOT EXISTS 'app_pacientes'@'%' IDENTIFIED BY 'password_seguro';
GRANT ALL PRIVILEGES ON pacientes_monitoreo.* TO 'app_pacientes'@'%';
FLUSH PRIVILEGES;
