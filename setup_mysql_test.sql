-- Prepare MySQL server for the test environment
-- Creates the database hbnb_test_db, user hbnb_test, and grants privileges

-- Create the test database if it does not already exist
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- Create the test user if it does not already exist
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

-- Grant all privileges on hbnb_test_db to hbnb_test
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';

-- Grant SELECT privilege on performance_schema to hbnb_test
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';

-- Apply the privilege changes
FLUSH PRIVILEGES;
