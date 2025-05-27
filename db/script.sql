CREATE DATABASE pwhappygreen_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'pwhappygreen_user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON pwhappygreen_db.* TO 'pwhappygreen_user'@'localhost';
FLUSH PRIVILEGES;