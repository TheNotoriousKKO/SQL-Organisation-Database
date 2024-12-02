--Insert Members
INSERT INTO Members (name, date_of_joining, membership_level)
VALUES 
    ('Alice Kowalska', '2022-01-15', 3),
    ('Bob Nowak', '2021-09-10', 2),
    ('Charlie Wiśniewski', '2020-06-01', 4),
    ('Diana Kamińska', '2023-03-20', 1);
--Insert Projects

INSERT INTO Projects (project_name, date_of_event)
VALUES 
    ('Engineering Competition', '2024-05-10'),
    ('Cultural Exchange', '2024-06-15'),
    ('Winter Course', '2024-02-05');
--Assign Members to Projects

INSERT INTO MemberProjects (member_id, project_name)
VALUES 
    (1, 'Engineering Competition'),
    (2, 'Engineering Competition'),
    (2, 'Cultural Exchange'),
    (3, 'Cultural Exchange'),
    (3, 'Winter Course'),
    (4, 'Winter Course');