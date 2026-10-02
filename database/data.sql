TRUNCATE TABLE
    comments,
    deviations,
    concern_types,
    severity,
    users
RESTART IDENTITY CASCADE;


INSERT INTO users (f_name, l_name, email, password_hash)
VALUES
    ('John', 'Smith', 'john.smith@example.com', 'dummy_hash_1'),
    ('Anna', 'Brown', 'anna.brown@example.com', 'dummy_hash_2'),
    ('Mark', 'Wilson', 'mark.wilson@example.com', 'dummy_hash_3'),
    ('Laura', 'Taylor', 'laura.taylor@example.com', 'dummy_hash_4');


INSERT INTO severity (name)
VALUES
    ('Low'),
    ('Medium'),
    ('High'),
    ('Critical');


INSERT INTO concern_types (name)
VALUES
    ('Safety Concern'),
    ('Installation Issue'),
    ('Quality Issue'),
    ('Material Issue'),
    ('Other');


INSERT INTO deviations (
    ship,
    concern_type_id,
    severity_id,
    description,
    status,
    deadline,
    submitted_by,
    assigned_to
)
VALUES
    (
        'Ship A',
        1,
        4,
        'Missing safety railing near the working area.',
        'Open',
        '2026-10-10',
        1,
        2
    ),
    (
        'Ship A',
        2,
        3,
        'Pipe support installed in the wrong position.',
        'In Progress',
        '2026-10-15',
        2,
        3
    ),
    (
        'Ship B',
        3,
        2,
        'Surface finish does not meet the required quality.',
        'Open',
        '2026-10-20',
        3,
        4
    ),
    (
        'Ship C',
        4,
        3,
        'Damaged material found during installation.',
        'Closed',
        '2026-09-30',
        4,
        1
    ),
    (
        'Ship B',
        5,
        1,
        'Minor issue requiring further inspection.',
        'Open',
        NULL,
        1,
        NULL
    );


INSERT INTO comments (
    deviation_id,
    user_id,
    comment_text
)
VALUES
    (1, 2, 'I will inspect this today.'),
    (1, 1, 'Please update the status after inspection.'),
    (2, 3, 'The installation team has been informed.'),
    (2, 2, 'Work is currently in progress.'),
    (3, 4, 'Quality inspection is scheduled for tomorrow.'),
    (4, 1, 'Material has been replaced. Issue can be closed.');