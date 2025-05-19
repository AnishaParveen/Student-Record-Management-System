import mysql.connector
from mysql.connector import Error

def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",  
            database="university_db"
        )
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def add_student(cursor, conn):
    print("\nEnter student details:")
    reg_no = input("Registration Number: ").strip()
    name = input("Name: ").strip()
    batch = input("Batch (e.g., 2022-2026): ").strip()
    year = int(input("Year (1-4): "))
    semester = int(input("Semester (1-8): "))
    cgpa = float(input("CGPA: "))
    department = input("Department: ").strip()
    phone = input("Phone Number: ").strip()
    address = input("Address: ").strip()
    email = input("Email: ").strip()
    dob = input("Date of Birth (YYYY-MM-DD): ").strip()

    query = """
    INSERT INTO students
    (reg_no, name, batch, year, semester, department, phone, address, cgpa, email, date_of_birth)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (reg_no, name, batch, year, semester, department, phone, address, cgpa, email, dob)
    cursor.execute(query, values)
    conn.commit()
    print("Student added successfully!")

def view_students(cursor):
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    if not rows:
        print("No student records found.")
        return
    print("\n--- Student Records ---")
    print(f"{'Reg No':15} {'Name':20} {'Batch':12} {'Year':4} {'Sem':4} {'Dept':25} {'Phone':12} {'CGPA':5} {'Email':25} {'DOB':10}")
    print("-"*130)
    for r in rows:
        print(f"{r[0]:15} {r[1]:20} {r[2]:12} {r[3]:4} {r[4]:4} {r[5]:25} {r[6]:12} {r[8]:5.2f} {r[9]:25} {str(r[10])}")
       
    
def update_cgpa(cursor, conn):
    reg_no = input("Enter Registration Number to update CGPA: ").strip()
    new_cgpa = float(input("Enter new CGPA: "))
    cursor.execute("UPDATE students SET cgpa = %s WHERE reg_no = %s", (new_cgpa, reg_no))
    conn.commit()
    if cursor.rowcount > 0:
        print("CGPA updated successfully!")
    else:
        print("Student not found.")

def delete_student(cursor, conn):
    reg_no = input("Enter Registration Number to delete: ").strip()
    cursor.execute("DELETE FROM students WHERE reg_no = %s", (reg_no,))
    conn.commit()
    if cursor.rowcount > 0:
        print("Student deleted successfully!")
    else:
        print("Student not found.")

def main():
    conn = connect_db()
    if conn is None:
        return
    cursor = conn.cursor()

    while True:
        print("\n--- Student Record System ---")
        print("1. Add Student")
        print("2. View Students")
        print("3. Update CGPA")
        print("4. Delete Student")
        print("5. Exit")

        choice = input("Choose an option: ").strip()
        if choice == '1':
            add_student(cursor, conn)
        elif choice == '2':
            view_students(cursor)
        elif choice == '3':
            update_cgpa(cursor, conn)
        elif choice == '4':
            delete_student(cursor, conn)
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
