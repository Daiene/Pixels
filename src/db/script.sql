DROP DATABASE pixels;
CREATE DATABASE IF NOT EXISTS pixels;
USE pixels;



CREATE TABLE IF NOT EXISTS usuario(
    user_id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(255) NOT NULL,
    user_email VARCHAR(255) NOT NULL UNIQUE,
    user_password VARCHAR(255) NOT NULL,
    user_type INT NOT NULL DEFAULT '1'
);



CREATE TABLE IF NOT EXISTS post(
    post_id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    post_title VARCHAR(255) NOT NULL,
    post_content TEXT NOT NULL,
    post_date DATE NOT NULL,
    post_img VARCHAR(255),
    post_status TINYINT(1) NOT NULL,
    user_id BIGINT NOT NULL
);



CREATE TABLE IF NOT EXISTS comentario(
    com_id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    com_title VARCHAR(255) NOT NULL,
    com_content TEXT NOT NULL,
    com_date DATE NOT NULL,
    post_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL
);



ALTER TABLE comentario ADD (
    FOREIGN KEY (user_id) REFERENCES usuario(user_id),
    FOREIGN KEY (post_id) REFERENCES post(post_id)
);



ALTER TABLE post ADD (
    FOREIGN KEY (user_id) REFERENCES usuario(user_id)
);