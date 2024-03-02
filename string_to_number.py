def convert_string_to_number(value, error_value=0):
    type_ = type(error_value)
    try:
        # First, attempt to convert the string to an integer
        return type_(value)
    except ValueError:
        try:
            # If that fails, attempt to convert it to a float
            return type_(error_value)
        except ValueError:
            # If both conversions fail, return 0
            return 0
