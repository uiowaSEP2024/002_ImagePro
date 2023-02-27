CREATE table users
(
    id serial,
    username VARCHAR(25) NOT NULL,
    last_login timestamp NOT NULL DEFAULT now(),
    PRIMARY KEY (id)
);

CREATE TABLE Jobs
(
    id serial,
    user_id int NOT NULL,
    completed_steps int NOT NULL,
    remaining_steps int NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users(id) on DELETE CASCADE
);