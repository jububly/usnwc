from primary_key_generator import primary_key
from pg_functions import pg_connect, pg_disconnect


def training_menu():
    while True:
        choice = input("Choose an option: (add, view, update, back)\n").strip().lower()
        if choice == 'add':
            training_type = str.upper(input("Choose an option: (intro, obs, ho, checkoff, school (guide school, SL training, workshop, continued_ed), break)\n"))
            if training_type == 'INTRO':
                resultless_training('INTRO')
            elif training_type == 'OBS':
                resultless_training('OBSERVATIONS')
            elif training_type == 'HO':
                resultless_training('HANDS-ON')
            #     resultful? hands-on + needs more?
            elif training_type == 'CHECKOFF':
                resultful_training('CHECKOFF')
            elif training_type == 'SCHOOL':
                school_training()
            else:
                raise
        elif str.upper(choice) == 'UPDATE':
            pass
        elif str.upper(choice) == 'BACK':
            print("Returning to main menu.")
            break
        else:
            print(f"Unknown choice: {choice!r}")


def training_note():
    note = str.upper(input("Notes?"))
    if note == '':
        note = None
    return note

def resultless_training(objective):
    loc = str.upper(input("What location? "))
    trainee = int(input("Trainee Foreign Key: "))
    trainer = int(input("Trainer Foreign Key: "))
    note = training_note()
    conn = pg_connect()
    if conn is None:
        raise RuntimeError("Could not connect to database")
    pkey = primary_key(pkey_type='training')
    sql = """
          INSERT INTO training
          (id, training_type, trainee_id, trainer_id,
           location, objective, note)
          VALUES
              (%s, 'FIELD_TRAINING', %s, %s, %s, %s, %s);
          """
    params = (pkey, trainee, trainer, loc, objective, note)
    print(f'{loc}, {trainee}, {trainer}, {objective}, {note}')
    with conn.cursor() as cursor:
        cursor.execute(sql, params)
        conn.commit()
        print(f"✔ Added {objective} at {loc} completed by {trainee} with {trainer} (training id={pkey})")
        pg_disconnect(conn)
    return


def resultful_training(objective):
    loc = str.upper(input("What location? "))
    trainee = int(input("Trainee Foreign Key: "))
    trainer = int(input("Trainer Foreign Key: "))
    result = int(input("Result?"))
    result_list = ['PASSED', 'FAILED', 'READY', 'PASS -- AWAITING QUIZ', 'COMPLETED', 'INCOMPLETED']
    result_str = result_list[(result - 1)]
    note = training_note()
    conn = pg_connect()
    if conn is None:
        raise RuntimeError("Could not connect to database")
    pkey = primary_key(pkey_type='training')
    sql = """
          INSERT INTO training
          (id, training_type, trainee_id, trainer_id,
           location, objective, result, note)
          VALUES
              (%s, 'FIELD_TRAINING', %s, %s, %s, %s, %s, %s);
          """
    params = (pkey, trainee, trainer, loc, objective, result, note)
    print(f'{loc}, {trainee}, {trainer}, {objective}, {note}')
    with conn.cursor() as cursor:
        cursor.execute(sql, params)
        conn.commit()
        print(f"✔ Added {objective} at {loc} {result_str} by {trainee} with {trainer} (training id={pkey})")
        # todo: make trainee and trainer show their names. low prio bc this should be backend
        pg_disconnect(conn)
    return


def school_training():

    school_type = str.upper(input("Choose an option: (workshop, guideschool, con-ed"))
    if school_type == 'WORKSHOP':
        pass
    if school_type == 'GUIDESCHOOL':
        pass
    if school_type == 'CON-ED':
        pass
    loc = str.upper(input("What location? "))
    trainee = int(input("Trainee Foreign Key: "))
    trainer = int(input("Trainer Foreign Key: "))
    result = str.upper(input("Result?"))
    note = training_note()
    conn = pg_connect()
    if conn is None:
        raise RuntimeError("Could not connect to database")
    pkey = primary_key(pkey_type='training')
    sql = """
          INSERT INTO training
          (id, training_type, trainee_id, trainer_id,
           location, objective, result, note)
          VALUES
              (%s, 'FIELD_TRAINING', %s, %s, %s, %s, %s, %s);
          """
    params = (pkey, trainee, trainer, loc, school_type, result, note)
    print(f'{loc}, {trainee}, {trainer}, {school_type}, {note}')
    with conn.cursor() as cursor:
        cursor.execute(sql, params)
        conn.commit()
        print(f"✔ Added {school_type} at {loc} {result} by {trainee} with {trainer} (training id={pkey})")
        pg_disconnect(conn)
    return

# def obs(loc, trainee, trainer, note)


# def get_note():
#
#

# TODO: TIMESTAMP
# training input, training view, training edit

# training type
# training info
# commit to 'training'

# training view which lists trainings of a given trainee / trainer
