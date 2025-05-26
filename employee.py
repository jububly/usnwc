from primary_key_generator import primary_key
from pg_functions import pg_connect, pg_disconnect


def employee_menu():
    """
    Main prompt loop.  Breaks when the user types 'back'.
    """
    while True:

        choice = input("Choose an option: (add, update, view, back)\n").strip().lower()
        if choice == 'add':
            #  gives user the choice of adding a preferred name or not.
            display_wanted  = str.casefold(input("Display Name? (Y/N) - "))
            if display_wanted  == 'y':
                display_name = str.upper(input("Display Name - "))
            else:
                display_name = None
            first_name      = str.upper(input("First Name - "))
            last_name       = str.upper(input("Last Name - "))
            job_title       = str.upper(input("Job Title - "))
            permission_lvl  = int(input("Permission LVL - "))
            if permission_lvl >= 2:
                #  part-time guides all have generated IDs, full-time can input 1-150 if wanted.
                pref_wanted = str.casefold(input("preferred key? (Y/N)"))
                if pref_wanted == 'y':
                    pref = primary_key(input("pref. key"))
                else:
                    pref = primary_key(None, permission_lvl)
            else:
                pref = primary_key(None, permission_lvl)
            email           = str.upper(input("Email Address - "))
            dob             = str.upper(input("DOB (MM-DD-YYYY) - "))
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
            key = int(input("Employee ID to update: "))
            view_employee(key, True)



        elif choice == 'view':
            view_input = (input("Input employee key: "))
            while True:
                try:
                    key = int(view_input)
                    break
                except:
                    print("Input must be an integer")
                    view_input = (input("Input employee key (0 to break):"))
                    if view_input == 0:
                        raise
            #         todo: make this not connect to the database when breaking out of the loop
            view_employee(key, False)

        elif choice == 'back':
            print("Returning to main menu.")
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



def view_employee(key, update=False):
    conn = pg_connect()
    if conn is None:
        raise RuntimeError("Could not connect to database")
    sql = "select * from employee"

    # NOTE: this code could be optimized by using a WHERE clause in the select statement of the sql code that is formatted
    # to include the user's input, and this option should be visited.
    # this would essentially filter the entries through SQL code before it hits python, instead of pulling every entry and
    # later filtering through every single entry using an iterable cursor element.

    # this try + except block ensures that the entry is an integer. this could be taken a step further to ensure that the pkey is valid
    # but this should not be required if this is a back end command called by a front end api.

    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            for line in cursor:
                if line[0] == key:
                    saved_line = line
                    print(saved_line)
                    pass
                else:
                    pass
    # checks if 'key' matches the pkey of the entry and prints that entry

    except Exception as e:
        conn.rollback()
        print(f"✘ Failed to insert: {e}")
        raise
    finally:
        if update is True:
            array_value = int(input("array value (0-9) to be updated\n"))
            # todo: input validation, also cover invalid key case
            print(saved_line[array_value], '--> ', end='')
            updated_value = str(input())
            # dynamically updates whichever value is changed
            cols = ('id', 'employee_display', 'employee_first', 'employee_last', 'job_title', 'permission_lvl', 'status', 'last_active', 'email', 'dob')
            set_clause = ", ".join(f"{col} = %s" for col in cols)
            update_sql = f"""
            UPDATE employee
            set {set_clause}
            where id = %s"""
            update_params = []
            for value, item in enumerate(saved_line):
                if value == array_value:
                    update_params.append(updated_value)
                else:
                    update_params.append(item)
            print(update_params)
            update_params.append(saved_line[0])
            with conn.cursor() as cursor:
                cursor.execute(update_sql, update_params)
                conn.commit()
            # todo: input validation, also provide feedback when change is valid
        pg_disconnect(conn)

# Todo: create a list view? Pulls pkeys + First + Last names into a single string each, prints these strings out line by line

def update_employee(key, array_value, status='active'):
    pass
#       todo: integrate DB, this function should integrate with DB and change status of employees
#       consider changing function name, this will change the status of the employee by default
#       this can largely use the view_employee code, with an added layer on top that asks the user
#       which array value they want to update, followed by a prompt that pulls the necessary data
#       data type and allows for input. Maybe combine this and view_employee?
#       instead of combining these, make view_employee call update_employee if the user would like
#       to update the array values of an entry.
