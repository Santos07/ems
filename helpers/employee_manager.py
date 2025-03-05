from nbformat.v1.nbjson import write

from helpers.database import Database

import csv


class EmployeeManager:
    def __init__(self):
        self.db = Database()

    def add_employee(self, name, age, department, salary):
        conn = self.db.connect_database()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO employees (name, age, department, salary) VALUES
                (%s,%s,%s,%s)
            """
            cursor.execute(query, (name, age, department, salary))
            conn.commit()
            print(f"Employee : {name} added successfully.")

        except Exception as e:
            print(f"Error Adding Employee: {e}")

        finally:
            self.db.close()

    def view_employees(self):
        conn = self.db.connect_database()

        if not conn:
            return

        try:
            cursor = conn.cursor()
            query = """
                SELECT * FROM employees
            """
            cursor.execute(query)
            employees = cursor.fetchall()

            print("\n----------- Employees List ---------")

            for emp in employees:
                print(f"ID: {emp[0]}, Name: {emp[1]}, Age: {emp[2]}, Department: {emp[3]}, Salary: {emp[4]}")
            return employees

        except Exception as e:
            print(f"Error Fetching Employees Record: {e}")

        finally:
            self.db.close()

    def search_employee(self, name=None, department=None):
        conn = self.db.connect_database()

        if not conn:
            return

        try:
            cursor = conn.cursor()
            query = """
                        SELECT * FROM employees WHERE name=%s OR department=%s
                    """
            cursor.execute(query, (name, department))
            employees = cursor.fetchall()

            if employees:
                print("\n------------ Search Result -----------")

                for emp in employees:
                    print(f"ID: {emp[0]}, Name: {emp[1]}, Age: {emp[2]}, Department: {emp[3]}, Salary: {emp[4]}")
            else:
                print("\n------- No Record Found -----------")

        except Exception as e:
            print(f"Error Fetching Employee Record: {e}")

        finally:
            self.db.close()

    def update_employee(self, emp_id, name=None, department=None, age=None, salary=None):
        conn = self.db.connect_database()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            select_query = """
                        SELECT count(*) FROM employees WHERE id=%s
                    """
            cursor.execute(select_query, (emp_id,))
            count = cursor.fetchone()[0]

            if count == 1:
                # Dynamically build the update query based on provided parameters
                update_query = "UPDATE employees SET "
                update_values = []

                if name is not None:
                    update_query += "name=%s, "
                    update_values.append(name)

                if department is not None:
                    update_query += "department=%s, "
                    update_values.append(department)

                if age is not None:
                    update_query += "age=%s, "
                    update_values.append(int(age))

                if salary is not None:
                    update_query += "salary=%s, "
                    update_values.append(float(salary))

                # Remove the last comma and space
                update_query = update_query.rstrip(", ")

                # Add the WHERE clause to the update query
                update_query += " WHERE id=%s"
                update_values.append(emp_id)

                print("---- update query ----- ", update_query)
                print("---- update values ----- ", update_values)

                # Execute the update query
                cursor.execute(update_query, tuple(update_values))

                # Commit the changes
                conn.commit()
                print("Record Updated Successfully.")

            else:
                print(f"\nEmployee with a id: {emp_id} not Found. Please try again.")

        except Exception as e:
            print(f"Error Updating Employee Record: {e}")

        finally:
            self.db.close()

    def delete_employee(self, emp_id):
        conn = self.db.connect_database()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            select_query = """
                                    SELECT count(*) FROM employees WHERE id=%s
                                """
            cursor.execute(select_query, (emp_id,))
            count = cursor.fetchone()[0]

            if count == 1:
                delete_query = """
                    DELETE FROM employees WHERE id=%s
                """
                # Execute the update query
                cursor.execute(delete_query, (emp_id,))

                # Commit the changes
                conn.commit()
                print("Record Deleted Successfully.")
            else:
                print(f"\nEmployee with a id: {emp_id} not Found. Please try again.")

        except Exception as e:
            print(f"Error Updating Employee Record: {e}")

        finally:
            self.db.close()

    def view_salary_statistics(self):
        conn = self.db.connect_database()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            query = """
                        SELECT MAX(salary), MIN(salary), AVG(salary)
                        FROM employees
                    """
            cursor.execute(query)
            result = cursor.fetchall()

            if result:
                print("\n----  Result ---------")
                for record in result:
                    print(f"Max Salary: {record[0]}")
                    print(f"Min Salary: {record[1]}")
                    print(f"Avg Salary: {format(record[2], '.2f')}")

        except Exception as e:
            print(f"Error Fetching Statistics: {e}")

        finally:
            self.db.close()

    def export_CSV(self):
        try:
            employees_data = self.view_employees()
            file_name = "employees.csv"

            if employees_data is None:
                raise ValueError("Error While fetching employees")

            headers = ['ID', 'Name', 'Age', 'Department', 'Salary']
            with open(file_name, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(headers)
                writer.writerows(employees_data)
            print(f"Data has been exported to {file_name}")
        except Exception as e:
            print(f"Error occured: {e}")
