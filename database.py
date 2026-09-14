import sqlite3

DB_NAME = "company.db"


def create_database():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    # Create employees table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            department TEXT NOT NULL,
            salary INTEGER NOT NULL
        )
    """)

    # Insert sample data only if table is empty
    cursor.execute("SELECT COUNT(*) FROM employees")
    count = cursor.fetchone()[0]

    if count == 0:
        employees = [
            (101, "Aman", "Python Developer", "Engineering", 65000),
            (102, "Rahul", "Data Engineer", "Engineering", 72000),
            (103, "Priya", "HR Manager", "HR", 68000),
            (104, "Neha", "QA Engineer", "Testing", 61000),
            (105, "Arjun", "Backend Developer", "Engineering", 75000),
        ]

        cursor.executemany("""
            INSERT INTO employees
            (id, name, role, department, salary)
            VALUES (?, ?, ?, ?, ?)
        """, employees)

    connection.commit()
    connection.close()


def query_database(sql_query: str):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    try:
        cursor.execute(sql_query)
        rows = cursor.fetchall()

        columns = [description[0] for description in cursor.description]

        results = []

        for row in rows:
            results.append(dict(zip(columns, row)))

        return results

    except Exception as e:
        return f"Database error: {e}"

    finally:
        connection.close()