-- Удаление таблицы экспонатов
DROP TABLE exhibits;

-- Удаление таблицы комментариев
DROP TABLE comments;

-- Создание таблицы экспонатов
CREATE TABLE exhibits (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    label INT NOT NULL
);

-- Создание таблицы комментариев
CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    comment TEXT NOT NULL,
    exhibit_id INT NOT NULL,
    FOREIGN KEY (exhibit_id) REFERENCES exhibits(id) ON DELETE CASCADE
);
