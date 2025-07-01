from tabulate import tabulate
from datetime import datetime

# Initial employee data
employee_data = [
    {
        "id": "1",
        "name": "Kesuma",
        "position": "General Manager",
        "salary": 10000000,
        "attendance": None,
        "projects": [],
        "attendance_history": [],
        "performance_grade": None
    },
    {
        "id": "2",
        "name": "Tengil",
        "position": "Assistant Manager",
        "salary": 5000000,
        "attendance": None,
        "projects": [],
        "attendance_history": [],
        "performance_grade": None
    },
    {
        "id": "3",
        "name": "Abdul",
        "position": "Project Manager",
        "salary": 5000000,
        "attendance": None,
        "projects": [],
        "attendance_history": [],
        "performance_grade": None
    }
]

def grade_to_salary_adjustment(grade):
    """
    Convert performance grade to percentage adjustment in salary.
    """
    if grade == 'A': 
        return 0.10
    elif grade == 'B':
        return 0.05
    elif grade == 'C':
        return 0
    elif grade == 'D':
        return -0.05
    elif grade == 'E':
        return -0.10
    return None

def create_employee():
    """
    Create a new employee and add to employee_data.
    """
    while True:
        id_ = input("\nEnter Employee ID: ")
        if any(e['id'] == id_ for e in employee_data):
            print("ID already exists. Please enter a different ID.")
            continue
        break
    name = input("Name: ").title().strip()
    position = input("Position: ").title().strip()
    while True:
        try:
            salary = int(input("Salary: "))
            break
        except:
            print("Salary must be a number!")
    employee = {
        "id": id_,
        "name": name,
        "position": position,
        "salary": salary,
        "attendance": None,
        "projects": [],
        "attendance_history": [],
        "performance_grade": None
    }
    employee_data.append(employee)
    print("\n✅ Employee successfully added.")

def show_employee_details(e):
    """
    Show full details, attendance, and projects for a single employee.
    """
    print("\n" + "="*50)
    print(f" EMPLOYEE DATA: {e['name'].upper()} (ID: {e['id']})")
    print(tabulate([[
        e['id'], e['name'], e['position'], f"Rp{e['salary']:,}", e['attendance'] or '-', e['performance_grade'] or '-'
    ]], headers=["ID", "Name", "Position", "Salary", "Attendance", "Performance Grade"], tablefmt="grid"))

    # Attendance History
    print("\n Recent Attendance History:")
    if e['attendance_history']:
        print(tabulate(
            [[r['date'], r['status']] for r in e['attendance_history'][-3:]],
            headers=["Date", "Status"], tablefmt="fancy_grid"
        ))
    else:
        print("No attendance data yet.")

    # Projects
    print("\n Projects Participated:")
    if e['projects']:
        print(tabulate(
            [[p['name'], p['role']] for p in e['projects']],
            headers=["Project Name", "Role"], tablefmt="fancy_grid"
        ))
    else:
        print("No projects assigned.")

def employee_submenu(e):
    """
    Submenu for updating, deleting, or adding project/performance to employee.
    """
    while True:
        print("\n--- EMPLOYEE SUBMENU ---")
        print("1. Update Data")
        print("2. Delete Employee")
        print("3. Add Project")
        print("4. Add Performance Grade (+/- Salary)")
        print("5. Back")
        choice = input("Select: 1-5 ")
        if choice == '1':
            confirm = input("Are you sure you want to update this employee? (y/n): ").upper()
            if confirm == "Y":
                e['name'] = input(f"New Name ({e['name']}): ") or e['name']
                e['position'] = input(f"New Position ({e['position']}): ") or e['position']
                salary_input = input(f"New Salary ({e['salary']}): ")
                if salary_input:
                    try:
                        e['salary'] = int(salary_input)
                    except ValueError:
                        print("❌ Invalid salary.")
                        continue
                print("✅ Employee data updated.")
            else:
                print("Update cancelled.")
        elif choice == '2':
            confirm = input(f"Are you sure you want to delete this employee? (y/n): ").upper()
            if confirm == "Y":
                employee_data.remove(e)
                print("✅ Employee deleted.")
            else:
                print("Delete cancelled.")  
            return
        elif choice == '3':
            project_name = input("Project Name: ")
            role = input("Role: ")
            e['projects'].append({"name": project_name, "role": role})
            print("✅ Project data added.")
        elif choice == '4':
            while True:
                grade = input("Enter performance grade (A-E): ").upper()
                if grade in ['A','B','C','D','E']:
                    adjustment = grade_to_salary_adjustment(grade)
                    break
                else:
                    print("Invalid grade! Use letters A-E only.")
            if adjustment is not None:
                previous_salary = e['salary']
                e['salary'] = int(previous_salary * (1 + adjustment))
                e['performance_grade'] = grade
                print(f"✅ Salary updated from Rp{previous_salary:,} → Rp{e['salary']:,}")
        elif choice == '5':
            return
        else:
            print("Invalid option.")

def manage_employees():
    """
    Main menu for viewing and managing all employee data.
    """
    if not employee_data:
        print("No employee data available.")
        return
    print("\n[1] Show All Employees")
    print("[2] Manage Employee by ID")
    option = input("Choose an option: ")
    if option == '1':
        for e in employee_data:
            show_employee_details(e)
    elif option == '2':
        id_ = input("Enter Employee ID: ")
        for e in employee_data:
            if str(e['id']) == str(id_):
                show_employee_details(e)
                employee_submenu(e)
                return
        print("❌ Employee not found.")
    else:
        print("❌ Invalid option.")

def add_attendance():
    """
    Add today's attendance status for an employee.
    """
    print("\n[Add Today's Attendance]")
    id_ = input("Enter Employee ID: ")
    for e in employee_data:
        if str(e['id']) == str(id_):
            while True:
                attendance = input("Attendance (Present/Absent): ").title().strip()
                if attendance in ["Present", "Absent"]:
                    e['attendance'] = attendance
                    e['attendance_history'].append({
                        "date": datetime.today().strftime("%Y-%m-%d"),
                        "status": attendance
                    })
                    print("✅ Attendance recorded.")
                    return
                else:
                    print("❌ Only use 'Present' or 'Absent'.")
    print("❌ Employee not found.")

def search_employee():
    """
    Search employees by name or ID (partial match).
    """
    keyword = input("Enter name or ID to search: ").strip().lower()
    results = []
    for e in employee_data:
        if keyword in str(e['id']).lower() or keyword in e['name'].lower():
            results.append(e)
    if results:
        print(f"\nFound {len(results)} result(s):")
        for e in results:
            show_employee_details(e)
    else:
        print("❌ No matching employee found.")

def main_menu():
    """
    The main menu loop for the employee management application.
    """
    while True:
        print("\n=== MAIN MENU ===")
        print("1. Add Employee")
        print("2. View & Manage Employees")
        print("3. Attendance")
        print("4. Search Employee")
        print("5. Exit")
        choice = input("Choose (1-5): ")
        if choice == '1':
            create_employee()
        elif choice == '2':
            manage_employees()
        elif choice == '3':
            add_attendance()
        elif choice == '4':
            search_employee()
        elif choice == '5':
            print("Exiting program.")
            break
        else:
            print("Invalid choice.")

# Run the application
main_menu()


