-- prepares a MySQL server for the project


-- Environment variables
-- MYSQL_USER='RG_user' MYSQL_PWD='RG_password' MYSQL_HOST='localhost' MYSQL_DB='RG_db'
-- RG_API_HOST=0.0.0.0 RG_API_PORT=5000

-- Delete if the database `RG_DB` if it exists
DROP DATABASE IF EXISTS RG_DB;

-- And create a new database `RG_DB`
CREATE DATABASE RG_DB;

-- Create a `RG_USER` user to manage the database
CREATE USER IF NOT EXISTS 'RG_USER'@'localhost' IDENTIFIED BY 'RG_PASSWORD';

-- Provide ALL PRIVILEGES on `RG_DB` and `performance_schema` to `RG_USER` user to manipulate the database
GRANT ALL PRIVILEGES ON `RG_DB`.* TO 'RG_USER'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'RG_USER'@'localhost';

-- Flush the privileges
FLUSH PRIVILEGES;
