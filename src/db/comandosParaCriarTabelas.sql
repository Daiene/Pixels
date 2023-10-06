CREATE TABLE usuario(
    user_id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(255) NOT NULL,
    user_email VARCHAR(255) NOT NULL UNIQUE,
    user_password VARCHAR(255) NOT NULL,
    user_type INT NOT NULL DEFAULT '1',
);
CREATE TABLE postagens(
    post_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    post_title VARCHAR(255) NOT NULL,
    post_content TEXT NOT NULL,
    post_date DATE NOT NULL,
    post_img VARCHAR(255) NOT NULL,
    post_status TINYINT(1) NOT NULL,
    user_id int not null,
    FOREIGN KEY(user_id) REFERENCES usuario(user_id),
);
CREATE TABLE comentario(
    com_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    com_title VARCHAR(255) NOT NULL,
    com_content TEXT NOT NULL,
    com_date DATE NOT NULL,
    post_id int not null,
    user_id int not null
    FOREIGN KEY(post_id) REFERENCES postagens(post_id)
    FOREIGN KEY(user_id) REFERENCES usuario(user_id)
);