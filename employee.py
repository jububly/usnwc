from primary_key_generator import primary_key
from pg_functions import pg_connect, pg_disconnect


def employee_menu():
    """
    Main prompt loop.  Breaks when the user types 'back'.
    """
    while True:

        choice = input("Choose an option: (add, update, view, back): ").strip().lower()
        if choice == 'add':
            #  gives user the choice of adding a preferred name or not.
            display_wanted  = str.casefold(input("Display Name? (Y/N)"))
            if display_wanted  == 'y':
                display_name = str.upper(input("Display Name"))
            else:
                display_name = None
            first_name      = str.upper(input("First Name"))
            last_name       = str.upper(input("Last Name"))
            job_title       = str.upper(input("Job Title"))
            permission_lvl  = int(input("Permission LVL"))
            if permission_lvl >= 2:
                #  part-time guides all have generated IDs, full-time can input 1-150 if wanted.
                pref_wanted = str.casefold(input("preferred key? (Y/N)"))
                if pref_wanted == 'y':
                    pref = primary_key(input("pref. key"))
                else:
                    pref = primary_key(None, permission_lvl)
            else:
                pref = primary_key(None, permission_lvl)
            email           = str.upper(input("Email Address"))
            dob             = str.upper(input("DOB (MM-DD-YYYY)"))
            status_input    = int(input("Employee Status\n(1) active -- (2) inactive -- (3) onboarding -- (4) away"))
            if status_input == 1:
                status = 'ACTIVE'
            elif status_input == 2:
                status = 'INACTIVE'
            elif status_input == 3:
                status = 'ONBOARDING'
            elif status_input == 4:
                status = 'AWAY'
            # would this be better as a dictionary? or just extra complexity for no reason?
            else:
                print("Invalid option, breaking")
                break

            add_employee(
                pref,
                display_name,
                first_name,
                last_name,
                job_title,
                permission_lvl,
                email,
                dob,
                status
            )

        elif choice == 'update':
            key = int(input("Employee ID to deactivate: "))
            # todo: read database entries and add these to a dict with pkey as dict key.
            update_employee(key)

        elif choice == 'view':
            key = int(input("Employee ID to view: "))
            view_employee(key)

        elif choice == 'back':
            print("Exiting.")
            break

        else:
            print(f"Unknown choice: {choice!r}")

    return True


def add_employee(
        pkey,
        display_name,
        first_name,
        last_name,
        job_title,
        permission_lvl=1,
        email=None,
        dob=None,
        status='Active'
):
    """
    Opens one connection, inserts one row, commits, then closes.
    """
    conn = pg_connect()
    if conn is None:
        raise RuntimeError("Could not connect to database")

    sql = """
          INSERT INTO employee
          (id, employee_display, employee_first, employee_last,
           job_title, permission_lvl, status, email, dob)
          VALUES 
          (%s, %s, %s, %s, %s, %s, %s, %s, %s);
          """
    params = (pkey, display_name, first_name, last_name,
              job_title, permission_lvl, status, email, dob)

    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
        conn.commit()
        print(f"✔ Added {first_name} {last_name} (id={pkey})")
    except Exception as e:
        conn.rollback()
        print(f"✘ Failed to insert: {e}")
        raise
    finally:
        pg_disconnect(conn)

def update_employee(pkey, status='inactive'):
    pass
#       todo: integrate DB, this function should integrate with DB and change status of employees
#       consider changing function name, this will change the status of the employee by default
#       this can largely use the view_employee code, with an added layer on top that asks the user
#       which array value they want to update, followed by a prompt that pulls the necessary data
#       data type and allows for input. Maybe combine this and view_employee?
#       instead of combining these, make view_employee call update_employee if the user would like
#       to update the array values of an entry.

def view_employee(key):
    pass
    # todo: integrate DB, this will pull data from DB and open up a view that allows for input.
