from employee import employee_menu
from training import training_menu


# todo: make menus return to main_menu if 'back' is inputted.
def main_menu():
    menu_input = str.upper(input("Choose an option: (training, employee, break)"))
    if menu_input == "TRAINING":
        training_menu()
    elif menu_input == "EMPLOYEE":
        employee_menu()
    else:
        pass

main_menu()

# there is a current dissonance between what I would like the code to do and what it does.
# Current code requires terminal input every step of the way, with a front end to this code
# this would take on a different form, with input validation handled on the front end and
# this menu functionality only used as a kind of middleware that serves the front end and
# can commit data to the database.

# I also want the ability to create new tables through the front end.
# this is a longer term goal though.
