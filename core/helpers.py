def split_fullname(fullname):
    first_name, *last_parts = fullname.strip().split()
    last_name = " ".join(last_parts)

    return (first_name, last_name)
