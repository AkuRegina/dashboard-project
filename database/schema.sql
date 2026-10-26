DROP VIEW IF EXISTS comment_details;
DROP VIEW IF EXISTS deviation_details;


DROP TABLE IF EXISTS comments CASCADE;
DROP TABLE IF EXISTS deviations CASCADE;
DROP TABLE IF EXISTS concern_types CASCADE;
DROP TABLE IF EXISTS severity CASCADE;
DROP TABLE IF EXISTS users CASCADE;


CREATE TABLE users (
    user_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    f_name VARCHAR(100) NOT NULL,
    l_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);


CREATE TABLE severity (
    severity_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);


CREATE TABLE concern_types (
    concern_type_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);


CREATE TABLE deviations (
    deviation_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    ship VARCHAR(100),

    concern_type_id INTEGER NOT NULL,
    severity_id INTEGER NOT NULL,

    description TEXT NOT NULL,

    status VARCHAR(20) NOT NULL DEFAULT 'Open'
        CHECK (status IN ('Open', 'In Progress', 'Closed')),

    deadline DATE,

    submitted_by INTEGER NOT NULL,
    assigned_to INTEGER,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (concern_type_id)
        REFERENCES concern_types(concern_type_id),

    FOREIGN KEY (severity_id)
        REFERENCES severity(severity_id),

    FOREIGN KEY (submitted_by)
        REFERENCES users(user_id),

    FOREIGN KEY (assigned_to)
        REFERENCES users(user_id)
);


CREATE TABLE comments (
    comment_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    deviation_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,

    comment_text TEXT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (deviation_id)
        REFERENCES deviations(deviation_id)
        ON DELETE CASCADE,

    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
);


CREATE VIEW deviation_details AS
SELECT
    d.deviation_id,
    d.ship,

    d.concern_type_id,
    ct.name AS concern_type,

    d.severity_id,
    s.name AS severity,

    d.description,
    d.status,
    d.deadline,

    d.submitted_by,
    CONCAT(submitter.f_name, ' ', submitter.l_name) AS submitted_by_name,

    d.assigned_to,
    CONCAT(assignee.f_name, ' ', assignee.l_name) AS assigned_to_name,

    d.created_at

FROM deviations d

JOIN concern_types ct
    ON d.concern_type_id = ct.concern_type_id

JOIN severity s
    ON d.severity_id = s.severity_id

JOIN users submitter
    ON d.submitted_by = submitter.user_id

LEFT JOIN users assignee
    ON d.assigned_to = assignee.user_id;


CREATE VIEW comment_details AS
SELECT
    c.comment_id,
    c.deviation_id,

    c.user_id,
    CONCAT(u.f_name, ' ', u.l_name) AS user_name,

    c.comment_text,
    c.created_at

FROM comments c

JOIN users u
    ON c.user_id = u.user_id;