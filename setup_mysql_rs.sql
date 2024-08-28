-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS RG_db;
CREATE USER IF NOT EXISTS 'RG_user'@'localhost' IDENTIFIED BY 'RG_password';
GRANT ALL PRIVILEGES ON `RG_db`.* TO 'RG_user'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'RG_user'@'localhost';
FLUSH PRIVILEGES;
