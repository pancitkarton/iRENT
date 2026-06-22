import re

def validate_input(P, mode, length=20):
    if P == "": return True

    if len(P) > length:
        return False

    # Only enforce a length limit if one is explicitly provided
    if length is not None and len(P) > length:
        return False

    if mode == "numbers":
        return P.isdigit() and len(P) <= length

    if mode == "suffix":
        return all(x.isalpha() or x.isspace() or x == "." for x in P)

    if mode == "alpha":
        return all(x.isalpha() or x.isspace() for x in P)

    if mode == "email":
        return bool(re.match(r'^[a-zA-Z0-9._%+-@]*$', P))

    if mode == "username":
        if " " in P: return False
        return len(P) <= length

    return True