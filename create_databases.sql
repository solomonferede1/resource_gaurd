-- **************************** MySQL ***************************
-- ************ ResourceGuard by solomonf1227@gmail.com *********


-- ******** Create a database for the project `resource_gaurd`***********

CREATE DATABASE IF NOT EXISTS `resource_gaurd`;

-- ******** Change the database to `resource_gaurd` *********************

USE resource_gaurd;

-- ***************** Create the tables ***********************************

-- **************** `Employee` table *************************************

CREATE TABLE IF NOT EXISTS `Employee`
(
 `id`        int NOT NULL AUTO_INCREMENT,
 `first_name` varchar(60) NOT NULL,
 `last_name`  varchar(60) NOT NULL,
 `role`      varchar(60) NOT NULL,
 `email`     varchar(60) UNIQUE NOT NULL,
 `phone`     varchar(20) UNIQUE NULL,
 `salary`    decimal(10, 2) NOT NULL,
 `date_hired` date NOT NULL,

PRIMARY KEY (`id`)
);


-- **************** `Payroll` table *************************************

CREATE TABLE IF NOT EXISTS `Payroll`
(
 `id`             int NOT NULL AUTO_INCREMENT,
 `total_work_hours` decimal(6, 2) NOT NULL,  -- Monthly total work hours, increased decimal length
 `salary`         decimal(10, 2) NOT NULL,
 `net_salary`     decimal(10, 2) NOT NULL,
 `payment_date`   date NOT NULL,
 `employee_id`    int NOT NULL,

PRIMARY KEY (`id`),
KEY `FK_1` (`employee_id`),
CONSTRAINT `FK_2` FOREIGN KEY `FK_1` (`employee_id`) REFERENCES `Employee` (`id`)
);

-- **************** `Attendance` table *************************************

CREATE TABLE IF NOT EXISTS `Attendance`
(
 `id`              int NOT NULL AUTO_INCREMENT,
 `check_in_time`   datetime NOT NULL,
 `check_out_time`  datetime NOT NULL,
 `total_work_hours` decimal(4, 2) GENERATED ALWAYS AS (
     TIMESTAMPDIFF(HOUR, check_in_time, check_out_time)
 ) STORED,  -- Total work hours per day calculated from check in/out times
 `attendance_date` date NOT NULL,
 `status`          boolean NOT NULL,
 `employee_id`     int NOT NULL,

PRIMARY KEY (`id`),
KEY `FK_1` (`employee_id`),
CONSTRAINT `FK_9_1` FOREIGN KEY `FK_1` (`employee_id`) REFERENCES `Employee` (`id`)
);

-- **************** `Catagory` table *************************************

CREATE TABLE IF NOT EXISTS `Category`
(
 `id`           int NOT NULL AUTO_INCREMENT,
 `category_name` varchar(60) NOT NULL,
 `created_at`    datetime NOT NULL,
 `updated_at`    datetime NOT NULL,

PRIMARY KEY (`id`)
);

-- **************** `Product` table *************************************

CREATE TABLE IF NOT EXISTS `Product`
(
 `id`             int NOT NULL AUTO_INCREMENT,
 `product_name`   varchar(60) NOT NULL,
 `product_type`   varchar(60) NOT NULL,
 `quantity`       int NOT NULL,
 `price`          decimal(10, 2) NOT NULL,
 `production_date` datetime NOT NULL,
 `created_at`      datetime NOT NULL,
 `updated_at`      datetime NOT NULL,
 `deleted_at`      datetime DEFAULT NULL,  -- Soft delete column
 `category_id`    int NOT NULL,

PRIMARY KEY (`id`),
KEY `FK_1` (`category_id`),
CONSTRAINT `FK_4` FOREIGN KEY `FK_1` (`category_id`) REFERENCES `Category` (`id`)
);

-- **************** `Inventory` table *************************************

CREATE TABLE IF NOT EXISTS `Inventory`
(
 `id`              int NOT NULL AUTO_INCREMENT,
 `item_type`       enum('rawmaterial', 'product') NOT NULL,
 `quantity_in_stock` bigint NOT NULL,
 `updated_at`       datetime NOT NULL,
 `product_id`       int NOT NULL,

PRIMARY KEY (`id`),
KEY `FK_1` (`product_id`),
CONSTRAINT `FK_3` FOREIGN KEY `FK_1` (`product_id`) REFERENCES `Product` (`id`)
);

-- **************** `Supplier` table *************************************

CREATE TABLE IF NOT EXISTS `Supplier`
(
 `id`          int NOT NULL AUTO_INCREMENT,
 `name`        varchar(60) NOT NULL,
 `contact_info` varchar(60) NOT NULL,
 `email`       varchar(60) NOT NULL,
 `address`     varchar(200) NOT NULL,

PRIMARY KEY (`id`)
);

-- **************** `RawMaterial` table *************************************

CREATE TABLE IF NOT EXISTS `RawMaterial`
(
 `id`           int NOT NULL AUTO_INCREMENT,
 `material_name` varchar(60) NOT NULL,
 `quantity`     int NOT NULL,
 `unit_price`    decimal(15, 2) NOT NULL,
 `created_at`    datetime NOT NULL,
 `updated_at`    datetime NOT NULL,
 `supplier_id`   int NOT NULL,

PRIMARY KEY (`id`),
KEY `FK_1` (`supplier_id`),
CONSTRAINT `FK_5` FOREIGN KEY `FK_1` (`supplier_id`) REFERENCES `Supplier` (`id`)
);

-- **************** `ProductTransaction` table *************************************

CREATE TABLE IF NOT EXISTS `ProductTransaction`
(
 `id`                     int NOT NULL AUTO_INCREMENT,
 `transaction_type`       enum('add', 'withdraw') NOT NULL,
 `quantity`               int NOT NULL,
 `transaction_date`       datetime NOT NULL,
 `transaction_by_employee_id` int NOT NULL,
 `product_id`             int NOT NULL,

PRIMARY KEY (`id`),
KEY `FK_1` (`transaction_by_employee_id`),
CONSTRAINT `FK_7` FOREIGN KEY `FK_1` (`transaction_by_employee_id`) REFERENCES `Employee` (`id`),
KEY `FK_2` (`product_id`),
CONSTRAINT `FK_8` FOREIGN KEY `FK_2` (`product_id`) REFERENCES `Product` (`id`)
);

-- **************** `RawMaterialTransaction` table *************************************

CREATE TABLE IF NOT EXISTS `RawMaterialTransaction`
(
 `id`                     int NOT NULL AUTO_INCREMENT,
 `transaction_type`       enum('add', 'withdraw') NOT NULL,
 `quantity`               int NOT NULL,
 `transaction_date`       datetime NOT NULL,
 `transaction_by_employee_id` int NOT NULL,
 `raw_material_id`        int NOT NULL,

PRIMARY KEY (`id`),
KEY `FK_1` (`transaction_by_employee_id`),
CONSTRAINT `FK_9` FOREIGN KEY `FK_1` (`transaction_by_employee_id`) REFERENCES `Employee` (`id`),
KEY `FK_2` (`raw_material_id`),
CONSTRAINT `FK_10` FOREIGN KEY `FK_2` (`raw_material_id`) REFERENCES `RawMaterial` (`id`)
);
