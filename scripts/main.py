from prettytable import PrettyTable
import psycopg2
from config import DATABASE


def connect_to_db():
    """
    Establishes a connection to the PostgreSQL database using credentials from the config file.
    """
    return psycopg2.connect(
        dbname=DATABASE["dbname"],
        user=DATABASE["user"],
        password=DATABASE["password"],
        host=DATABASE["host"],
        port=DATABASE["port"]
    )


def list_all_projects_with_members():
    """
    Lists all projects and their contributing members.
    """
    query = """
        SELECT p.project_name, STRING_AGG(m.name, ', ') AS members
        FROM Projects p
        LEFT JOIN MemberProjects mp ON p.project_name = mp.project_name
        LEFT JOIN Members m ON mp.member_id = m.id
        GROUP BY p.project_name
        ORDER BY p.project_name;
    """
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    table = PrettyTable()
    table.field_names = ["Project Name", "Members"]
    for row in results:
        project_name, members = row
        table.add_row([project_name, members or "None"])

    print("\nProjects and Their Members")
    print(table)


def list_all_members():
    """
    Lists all members in the Members table.
    """
    query = "SELECT * FROM Members;"
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    table = PrettyTable()
    table.field_names = ["ID", "Name", "Date of Joining", "Membership Level"]
    for row in results:
        table.add_row(row)

    print("\nAll Members")
    print(table)


def list_members_by_level():
    """
    Lists all members of a specific membership level.
    """
    membership_level = int(input("Enter membership level (1-4): "))
    query = """
        SELECT id, name, date_of_joining
        FROM Members
        WHERE membership_level = %s
        ORDER BY name;
    """
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(query, (membership_level,))
    results = cursor.fetchall()
    conn.close()

    table = PrettyTable()
    table.field_names = ["ID", "Name", "Date of Joining"]
    for row in results:
        table.add_row(row)

    print(f"\nMembers at Level {membership_level}")
    print(table)
def add_new_member():
    """
    Adds a new member to the Members table.
    """
    name = input("Enter the member's name: ")
    date_of_joining = input("Enter the date of joining (YYYY-MM-DD): ")
    membership_level = int(input("Enter membership level (1-4): "))

    query = """
        INSERT INTO Members (name, date_of_joining, membership_level)
        VALUES (%s, %s, %s)
    """
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        cursor.execute(query, (name, date_of_joining, membership_level))
        conn.commit()
        print(f"New member '{name}' added successfully!")
    except Exception as e:
        conn.rollback()
        print(f"Error adding member: {e}")
    finally:
        conn.close()


def add_new_project():
    """
    Adds a new project to the Projects table.
    """
    project_name = input("Enter the project name: ")
    date_of_event = input("Enter the date of the project (YYYY-MM-DD): ")

    query = """
        INSERT INTO Projects (project_name, date_of_event)
        VALUES (%s, %s)
    """
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        cursor.execute(query, (project_name, date_of_event))
        conn.commit()
        print(f"New project '{project_name}' added successfully!")
    except Exception as e:
        conn.rollback()
        print(f"Error adding project: {e}")
    finally:
        conn.close()


def assign_member_to_project():
    """
    Assigns a member to a project in the MemberProjects table.
    """
    list_all_members()
    member_id = int(input("Enter the member ID: "))

    query_projects = "SELECT project_name FROM Projects;"
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(query_projects)
    projects = cursor.fetchall()
    conn.close()

    print("\nAvailable Projects:")
    for project in projects:
        print(f" - {project[0]}")
    project_name = input("Enter the project name: ")

    query = """
        INSERT INTO MemberProjects (member_id, project_name)
        VALUES (%s, %s)
    """
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        cursor.execute(query, (member_id, project_name))
        conn.commit()
        print(f"Member ID {member_id} assigned to project '{project_name}' successfully!")
    except Exception as e:
        conn.rollback()
        print(f"Error assigning member to project: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    while True:
        print("\nBEST Łódź Member Management")
        print("1. List all projects with their members")
        print("2. List all members")
        print("3. List members by membership level")
        print("4. Add a new member")
        print("5. Add a new project")
        print("6. Assign a member to a project")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            list_all_projects_with_members()
        elif choice == "2":
            list_all_members()
        elif choice == "3":
            list_members_by_level()
        elif choice == "4":
            add_new_member()
        elif choice == "5":
            add_new_project()
        elif choice == "6":
            assign_member_to_project()
        elif choice == "7":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")