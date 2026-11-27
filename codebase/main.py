from datetime import datetime

# Employee records and leave balances are stored in a dictionary.
# Each leave request is counted inclusively (both start and end dates).
employees = {
    "E101": {
        "name": "Amit",
        "leave_balance": {
            "Casual": 12,
            "Sick": 10,
            "Earned": 15
        }
    }
}

LEAVE_TYPES = ("Casual", "Sick", "Earned")


def parse_date(date_text):
    """Parse a date strictly in YYYY-MM-DD format."""
    try:
        parsed_date = datetime.strptime(date_text, "%Y-%m-%d").date()
        # strptime can accept some non-zero-padded values; enforce exact format.
        if parsed_date.strftime("%Y-%m-%d") != date_text:
            raise ValueError
        return parsed_date
    except ValueError:
        raise ValueError("Invalid date format. Please use YYYY-MM-DD.")


def calculate_leave_days(from_date, to_date):
    """Return the inclusive number of calendar days between two dates."""
    start = parse_date(from_date)
    end = parse_date(to_date)

    if end < start:
        raise ValueError("To-date cannot be before from-date.")

    return (end - start).days + 1


def display_balance(employee_id):
    """Display all available leave balances for an employee."""
    employee = employees.get(employee_id.upper())

    if employee is None:
        print("Invalid employee ID.")
        return

    balances = employee["leave_balance"]
    print(f"\nLeave Balance for {employee_id.upper()} ({employee['name']}):")
    for leave_type in LEAVE_TYPES:
        print(f"{leave_type}: {balances[leave_type]} days")
    print()


def apply_leave():
    """Collect, validate, and process one employee leave application."""
    employee_id = input("Enter Employee ID: ").strip().upper()

    if employee_id not in employees:
        print("Invalid employee ID.")
        return

    leave_type_input = input("Enter Leave Type (Casual/Sick/Earned): ").strip()
    leave_type = next(
        (item for item in LEAVE_TYPES
         if item.lower() == leave_type_input.lower()),
        None
    )

    if leave_type is None:
        print("Invalid leave type. Choose Casual, Sick, or Earned.")
        return

    from_text = input("Enter From Date (YYYY-MM-DD): ").strip()
    to_text = input("Enter To Date (YYYY-MM-DD): ").strip()

    try:
        number_of_days = calculate_leave_days(from_text, to_text)
    except ValueError as error:
        print(error)
        return

    balance = employees[employee_id]["leave_balance"][leave_type]

    if number_of_days <= balance:
        employees[employee_id]["leave_balance"][leave_type] -= number_of_days
        remaining = employees[employee_id]["leave_balance"][leave_type]
        print(
            f"Leave approved: {number_of_days} days {leave_type} "
            f"| Balance {leave_type}: {remaining}"
        )
    else:
        print(
            f"Leave rejected. Requested: {number_of_days} days "
            f"| Available: {balance}"
        )


def add_employee():
    """Optional helper to add another employee through the console."""
    employee_id = input("Enter new Employee ID: ").strip().upper()

    if not employee_id:
        print("Employee ID cannot be empty.")
        return
    if employee_id in employees:
        print("This employee ID already exists.")
        return

    name = input("Enter employee name: ").strip()
    if not name:
        print("Employee name cannot be empty.")
        return

    employees[employee_id] = {
        "name": name,
        "leave_balance": {
            "Casual": 12,
            "Sick": 10,
            "Earned": 15
        }
    }
    print(f"Employee {employee_id} added successfully.")
    print("Default leave balances: Casual 12, Sick 10, Earned 15.")


def main():
    """Main menu of the Employee Leave Management System."""
    while True:
        print("========== EMPLOYEE LEAVE MANAGEMENT SYSTEM ==========")
        print("1. Apply for Leave")
        print("2. View Leave Balance")
        print("3. Add Employee")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            apply_leave()
        elif choice == "2":
            employee_id = input("Enter Employee ID: ").strip()
            display_balance(employee_id)
        elif choice == "3":
            add_employee()
        elif choice == "4":
            print("Thank you for using the Employee Leave Management System.")
            break
        else:
            print("Invalid menu option. Please enter 1, 2, 3, or 4.")

        print()


if __name__ == "__main__":
    main()
