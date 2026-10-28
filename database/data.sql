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
    assigned_to,
    blueprint_image_ref,
    issue_photo_ref,
    created_at
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
        2,
        'assets/blueprints/deviation_001.png',
        'assets/issues/deviation_001.jpg',
        '2026-07-02 09:15:00'
    ),
    (
        'Ship A',
        2,
        3,
        'Pipe support installed in the wrong position.',
        'In Progress',
        '2026-10-15',
        2,
        3,
        'assets/blueprints/deviation_002.png',
        'assets/issues/deviation_002.jpg',
        '2026-07-05 11:30:00'
    ),
    (
        'Ship B',
        3,
        2,
        'Surface finish does not meet the required quality.',
        'Open',
        '2026-10-20',
        3,
        4,
        'assets/blueprints/deviation_003.png',
        'assets/issues/deviation_003.jpg',
        '2026-07-08 14:20:00'
    ),
    (
        'Ship C',
        4,
        3,
        'Damaged material found during installation.',
        'Closed',
        '2026-09-30',
        4,
        1,
        'assets/blueprints/deviation_004.png',
        'assets/issues/deviation_004.jpg',
        '2026-07-11 08:45:00'
    ),
    (
        'Ship B',
        5,
        1,
        'Minor issue requiring further inspection.',
        'Open',
        NULL,
        1,
        NULL,
        'assets/blueprints/deviation_005.png',
        'assets/issues/deviation_005.jpg',
        '2026-07-15 13:10:00'
    ),

    (
        'Ship A',
        1,
        3,
        'Temporary access route is not properly secured.',
        'Closed',
        '2026-07-30',
        2,
        4,
        'assets/blueprints/deviation_006.png',
        'assets/issues/deviation_006.jpg',
        '2026-07-19 10:00:00'
    ),
    (
        'Ship C',
        2,
        2,
        'Cable tray is mounted outside the planned position.',
        'Closed',
        '2026-08-12',
        3,
        1,
        'assets/blueprints/deviation_007.png',
        'assets/issues/deviation_007.jpg',
        '2026-08-02 09:40:00'
    ),
    (
        'Ship B',
        3,
        3,
        'Weld quality does not meet inspection requirements.',
        'Closed',
        '2026-08-15',
        4,
        2,
        'assets/blueprints/deviation_008.png',
        'assets/issues/deviation_008.jpg',
        '2026-08-05 15:15:00'
    ),
    (
        'Ship A',
        4,
        2,
        'Incorrect material grade used for the bracket.',
        'Closed',
        '2026-08-18',
        1,
        3,
        'assets/blueprints/deviation_009.png',
        'assets/issues/deviation_009.jpg',
        '2026-08-08 12:30:00'
    ),
    (
        'Ship D',
        1,
        4,
        'Emergency exit area partially blocked.',
        'Closed',
        '2026-08-14',
        2,
        4,
        'assets/blueprints/deviation_010.png',
        'assets/issues/deviation_010.jpg',
        '2026-08-10 08:20:00'
    ),

    (
        'Ship C',
        2,
        2,
        'Ventilation duct installed too close to cable route.',
        'Closed',
        '2026-08-24',
        3,
        2,
        'assets/blueprints/deviation_011.png',
        'assets/issues/deviation_011.jpg',
        '2026-08-14 14:50:00'
    ),
    (
        'Ship B',
        3,
        1,
        'Paint layer thickness below specification.',
        'Closed',
        '2026-08-30',
        4,
        1,
        'assets/blueprints/deviation_012.png',
        'assets/issues/deviation_012.jpg',
        '2026-08-18 09:35:00'
    ),
    (
        'Ship D',
        4,
        3,
        'Steel plate shows visible surface damage.',
        'Closed',
        '2026-09-02',
        1,
        4,
        'assets/blueprints/deviation_013.png',
        'assets/issues/deviation_013.jpg',
        '2026-08-22 11:25:00'
    ),
    (
        'Ship A',
        1,
        3,
        'Protective cover missing from electrical equipment.',
        'Closed',
        '2026-09-10',
        2,
        3,
        'assets/blueprints/deviation_014.png',
        'assets/issues/deviation_014.jpg',
        '2026-09-01 10:10:00'
    ),
    (
        'Ship B',
        2,
        2,
        'Pipe penetration does not align with the planned opening.',
        'In Progress',
        '2026-09-15',
        3,
        1,
        'assets/blueprints/deviation_015.png',
        'assets/issues/deviation_015.jpg',
        '2026-09-04 13:45:00'
    ),

    (
        'Ship C',
        3,
        3,
        'Visible gap found between installed panels.',
        'Closed',
        '2026-09-17',
        4,
        2,
        'assets/blueprints/deviation_016.png',
        'assets/issues/deviation_016.jpg',
        '2026-09-07 08:30:00'
    ),
    (
        'Ship D',
        4,
        2,
        'Delivered pipe section contains surface damage.',
        'Closed',
        '2026-09-20',
        1,
        3,
        'assets/blueprints/deviation_017.png',
        'assets/issues/deviation_017.jpg',
        '2026-09-10 14:00:00'
    ),
    (
        'Ship A',
        5,
        1,
        'Unidentified obstruction found near installation area.',
        'Closed',
        '2026-09-25',
        2,
        4,
        'assets/blueprints/deviation_018.png',
        'assets/issues/deviation_018.jpg',
        '2026-09-14 09:05:00'
    ),
    (
        'Ship B',
        1,
        4,
        'Temporary platform has insufficient edge protection.',
        'In Progress',
        '2026-09-24',
        3,
        2,
        'assets/blueprints/deviation_019.png',
        'assets/issues/deviation_019.jpg',
        '2026-09-17 11:50:00'
    ),
    (
        'Ship C',
        2,
        3,
        'Equipment mounting position differs from blueprint.',
        'In Progress',
        '2026-09-29',
        4,
        1,
        'assets/blueprints/deviation_020.png',
        'assets/issues/deviation_020.jpg',
        '2026-09-21 15:10:00'
    ),

    (
        'Ship D',
        3,
        2,
        'Incorrect surface treatment detected.',
        'Closed',
        '2026-10-03',
        1,
        2,
        'assets/blueprints/deviation_021.png',
        'assets/issues/deviation_021.jpg',
        '2026-09-25 10:35:00'
    ),
    (
        'Ship A',
        4,
        3,
        'Material deformation detected before installation.',
        'In Progress',
        '2026-10-05',
        2,
        3,
        'assets/blueprints/deviation_022.png',
        'assets/issues/deviation_022.jpg',
        '2026-09-28 12:20:00'
    ),
    (
        'Ship B',
        1,
        4,
        'Safety barrier missing around an open floor section.',
        'Open',
        '2026-10-10',
        3,
        4,
        'assets/blueprints/deviation_023.png',
        'assets/issues/deviation_023.jpg',
        '2026-10-01 08:15:00'
    ),
    (
        'Ship C',
        2,
        3,
        'Pipe support spacing differs from installation requirements.',
        'In Progress',
        '2026-10-14',
        4,
        1,
        'assets/blueprints/deviation_024.png',
        'assets/issues/deviation_024.jpg',
        '2026-10-04 13:30:00'
    ),
    (
        'Ship D',
        3,
        2,
        'Door alignment is outside acceptable tolerance.',
        'Open',
        '2026-10-18',
        1,
        2,
        'assets/blueprints/deviation_025.png',
        'assets/issues/deviation_025.jpg',
        '2026-10-07 09:55:00'
    ),

    (
        'Ship A',
        4,
        3,
        'Insulation material damaged during installation.',
        'In Progress',
        '2026-10-20',
        2,
        3,
        'assets/blueprints/deviation_026.png',
        'assets/issues/deviation_026.jpg',
        '2026-10-10 14:40:00'
    ),
    (
        'Ship B',
        5,
        1,
        'Small clearance issue requires verification.',
        'Open',
        '2026-10-25',
        3,
        NULL,
        'assets/blueprints/deviation_027.png',
        'assets/issues/deviation_027.jpg',
        '2026-10-14 11:05:00'
    ),
    (
        'Ship C',
        1,
        4,
        'Loose temporary electrical cable creates a safety risk.',
        'Open',
        '2026-10-29',
        4,
        1,
        'assets/blueprints/deviation_028.png',
        'assets/issues/deviation_028.jpg',
        '2026-10-18 08:50:00'
    ),
    (
        'Ship D',
        2,
        2,
        'Bracket installed approximately 50 mm from planned position.',
        'In Progress',
        '2026-11-02',
        1,
        4,
        'assets/blueprints/deviation_029.png',
        'assets/issues/deviation_029.jpg',
        '2026-10-22 13:15:00'
    ),
    (
        'Ship A',
        3,
        3,
        'Final inspection found an unfinished surface area.',
        'Open',
        '2026-11-05',
        2,
        NULL,
        'assets/blueprints/deviation_030.png',
        'assets/issues/deviation_030.jpg',
        '2026-10-26 10:30:00'
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