def split_fullname(fullname):
    """
    Split a full name into first name and last name.

    The first word becomes the first name, remaining words are joined
    as the last name.
    """
    first_name, *last_parts = fullname.strip().split()
    last_name = " ".join(last_parts)

    return (first_name, last_name)
