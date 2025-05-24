import random

def primary_key(pref=None, permission_lvl=None):
    if pref is not None:
        # todo: and pref not in employees
        # todo: if permission_lvl > 1, 151-999, else 1001-99999
        return pref
    else:
        i = 0
        while True:
            i += 1
            preferred_value = random.randint(12, 21)
            # if preferred_value not in employees:
            return preferred_value
#   Todo: read database id's to validate p_keys
#     elif:
#         pg_connect()
#
