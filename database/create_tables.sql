-- Create Members table
CREATE TABLE Members (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    date_of_joining DATE NOT NULL,
    membership_level INT CHECK (membership_level BETWEEN 1 AND 4)
);

-- Create Projects table
CREATE TABLE Projects (
    project_name VARCHAR(100) PRIMARY KEY,
    date_of_event DATE NOT NULL
);

-- Create MemberProjects join table (many-to-many relationship)
CREATE TABLE MemberProjects (
    member_id INT REFERENCES Members(id) ON DELETE CASCADE,
    project_name VARCHAR(100) REFERENCES Projects(project_name) ON DELETE CASCADE,
    PRIMARY KEY (member_id, project_name)
);
