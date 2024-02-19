DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS users;
DROP TYPE IF EXISTS event_kind;

CREATE TYPE event_kind AS ENUM ('step', 'info', 'error');

CREATE table users
(
    id serial,
    username VARCHAR(25) NOT NULL,
    last_login timestamp NOT NULL DEFAULT now(),
    PRIMARY KEY (id)
);

CREATE table events
(
    id serial,
    user_id int not null,
    kind event_kind NOT NULL,
    job_id VARCHAR(25) NOT NULL,
    name VARCHAR(25) NOT NULL,
    created_at timestamp NOT NULL default now(),
    info jsonb,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users(id) on DELETE CASCADE
);


INSERT INTO users
    (id, username)
VALUES
    (1, 'anandgopal08'),
    (2, 'rexessilfie'),
    (3, 'mirabtel'),
    (4, 'bainwala');


INSERT INTO events
    (user_id, job_id, kind, name, info)
VALUES
    (1, 'abc', 'step', 'kidney scan', null),
    (1, 'abc', 'info', 'kidney scan info', '[{ "name": "Size", "value": "100mm"}, {"name": "Verdict", "value": "Healthy"}]'),
    (1, 'abc', 'step', 'image processing', null),
    (2, 'def', 'step', 'mri scan', null),
    (2, 'def', 'error', 'mri scan error', null),
    (3, 'ghi', 'step', 'lung exterior scan', null),
    (3, 'ghi', 'info', 'lung exterior scan info', '[{ "name": "Size", "value": "100mm"}, {"name": "Verdict", "value": "Needs Improvement"}]'),
    (4, 'klm', 'step', 'prostate scan', null);
