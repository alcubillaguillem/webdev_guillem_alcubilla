-- Demo data for slice 1. Every seeded account's password is "splitmate-demo".
INSERT INTO users (email, name, password_hash) VALUES
    ('ana@example.com',   'Ana',   '$2b$12$LVa01MkzyUwJhytiaI9wx..P5acbMNXSInnmi07zctSruiTrfcESG'),
    ('ben@example.com',   'Ben',   '$2b$12$LVa01MkzyUwJhytiaI9wx..P5acbMNXSInnmi07zctSruiTrfcESG'),
    ('carla@example.com', 'Carla', '$2b$12$LVa01MkzyUwJhytiaI9wx..P5acbMNXSInnmi07zctSruiTrfcESG');

INSERT INTO groups (name) VALUES
    ('Flat on Vitosha Blvd'),
    ('Weekend in Plovdiv'),
    ('Rila Monastery trip');

-- Ana owns the flat, is a member of Plovdiv, and is not in Rila.
INSERT INTO memberships (user_id, group_id, role) VALUES
    ((SELECT id FROM users WHERE email = 'ana@example.com'),   (SELECT id FROM groups WHERE name = 'Flat on Vitosha Blvd'), 'owner'),
    ((SELECT id FROM users WHERE email = 'ben@example.com'),   (SELECT id FROM groups WHERE name = 'Flat on Vitosha Blvd'), 'member'),
    ((SELECT id FROM users WHERE email = 'carla@example.com'), (SELECT id FROM groups WHERE name = 'Flat on Vitosha Blvd'), 'member'),
    ((SELECT id FROM users WHERE email = 'ben@example.com'),   (SELECT id FROM groups WHERE name = 'Weekend in Plovdiv'),   'owner'),
    ((SELECT id FROM users WHERE email = 'ana@example.com'),   (SELECT id FROM groups WHERE name = 'Weekend in Plovdiv'),   'member'),
    ((SELECT id FROM users WHERE email = 'carla@example.com'), (SELECT id FROM groups WHERE name = 'Rila Monastery trip'),  'owner');
