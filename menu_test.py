from pg_functions import(pg_connect, pg_disconnect)

conn = pg_connect()
if conn is None:
    raise RuntimeError("Could not connect to database")
sql = "select * from employee"

# NOTE: this code could be optimized by using a WHERE clause in the select statement of the sql code that is formatted
# to include the user's input, and this option should be visited.
# this would essentially filter the entries through SQL code before it hits python, instead of pulling every entry and
# later filtering through every single entry using an iterable cursor element.

view_input = (input("Input employee key: "))
while True:
    try:
        view_input = int(view_input)
        break
    except:
        print("Input must be an integer")
        view_input = (input("Input employee key (0 to break):"))
        if view_input == 0:
            raise
# this try + except block ensures that the entry is an integer. this could be taken a step further to ensure that the pkey is valid
# but this should not be required if this is a back end command called by a front end api.

try:
    with conn.cursor() as cursor:
        cursor.execute(sql)
        for line in cursor:
            if line[0] == view_input:
                print(line)
            else:
                pass
# checks if view_input matches the pkey of the entry and prints that entry

except Exception as e:
    conn.rollback()
    print(f"✘ Failed to insert: {e}")
    raise
finally:
    pg_disconnect(conn)

# Todo: create a list view? Pulls pkeys + First + Last names into a single string each, prints these strings out line by line
