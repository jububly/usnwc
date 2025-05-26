import random

PTLOW = 1001
PTHIGH = 99999
FTLOW = 151
FTHIGH = 999


def primary_key(pref=None, permission_lvl=None):
    """
    Primary key generator used in employee entry into the DB
    :param pref: if permission_lvl >= 2, user can include a pref value which allows them to input a pkey 1-150
    :param permission_lvl: permission lvl of the employee, 1 is PT, 2+ is FT. Determines the magnitude of the pkey
    :return: pkey value of the employee
    """
    if pref is not None:
        # todo: and pref not in employees
        return pref
    else:
        if permission_lvl == 1:
            preferred_value = random.randint(PTLOW, PTHIGH)
            return preferred_value
        elif permission_lvl >= 2:
            preferred_value = random.randint(FTLOW, FTHIGH)
            return preferred_value
        else:
            raise

#
