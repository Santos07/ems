from helpers.database import Database
from helpers.employee_manager import EmployeeManager
from models.admin import Admin
from models.users import User


def main():
    while True:
        print("\n------------ Welcome to Employee Management System ----------------")
        print("1. Login")
        print("2. Migrate Database")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            print("\n------------1. Logging IN  ----------------")
            username = input("Enter username: ")
            password = input("Enter password: ")

            user = Admin(username, password) if username == 'admin' else User(username, password)

            if not user.authenticate():
                print("Invalid Username and Password.")
                continue

            employee_manager = EmployeeManager()

            while True:
                print("\n------------ Menus ----------------")
                print("1. Add Employee")
                print("2. View Employee")
                print("3. Search Employee")
                print("4. Update Employee")
                print("5. Delete Employee")
                print("6. View Salary Statistics")
                print("7. Add User (Admin Only)")
                print("8. Export to CSV")
                print("9. Logout")

                option = input("\nSelect Option i.e. (1-9): ")

                if option == "1":
                    print("\n------------1. Add Employee ----------------")
                    name = input("Enter employee name: ")
                    age = int(input("Enter employee age: "))
                    department = input("Enter employee department: ")
                    salary = float(input("Enter employee salary: "))

                    employee_manager.add_employee(name, age, department, salary)

                elif option == "2":
                    print("\n------------2. View Employees ----------------")
                    employee_manager.view_employees()

                elif option == "3":
                    print("\n------------3. Search Employee Record ----------------")
                    name = input("Enter employee name (or leave blank): ")
                    department = input("Enter employee department (or leave blank): ")
                    employee_manager.search_employee(name or None, department or None)

                elif option == "4":
                    print("\n------------4. Update Employee Record ----------------")
                    print("\nEnter following detail for update purpose")
                    emp_id = int(input("Enter Employee ID: "))
                    name = input("Enter Employee Name (or leave blank): ")
                    department = input("Enter Department (or leave blank): ")
                    age = input("Enter Age (or leave blank): ")
                    salary = input("Enter Salary (or leave blank): ")
                    employee_manager.update_employee(emp_id, name or None, department or None, age or None,
                                                     salary or None)

                elif option == "5":
                    print("\n------------5. Delete Employee Record ----------------")
                    emp_id = int(input("Enter Employee ID: "))
                    employee_manager.delete_employee(emp_id)

                elif option == "6":
                    print("\n------------6. View Salary Statistics ----------------")
                    employee_manager.view_salary_statistics()

                elif option == "7":
                    if isinstance(user, Admin):
                        print("\n------------7. Add User ----------------")
                        new_uname = input("Enter Username: ")
                        new_pass = input("Enter Password: ")
                        new_role = input("Enter Role ('admin' or 'employee'):  ")
                        Admin.add_user(user, new_uname, new_pass,
                                       new_role) if new_role == "admin" or new_role == "employee" \
                            else print("Enter correct role i.e. either 'admin' or 'employee'")
                    else:
                        print("Only Admin User are allowed.")

                elif option == "8":
                    print("\n------------8. Search Employee ----------------")
                    employee_manager.export_CSV()

                elif option == "9":
                    print("\nLogging Out ...............")
                    break

                else:
                    print("Invalid Option, Please try again.")

        elif choice == "2":
            print("\n------------2. Migrating Database ----------------")
            database = Database()
            database.setup_database()

        elif choice == "3":
            print("\n------------3. Existing Program ----------------")
            break

        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()
