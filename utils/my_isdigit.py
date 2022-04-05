def my_isdigit(x) -> bool:
    try:
        float(x)
        return True
    except ValueError:
        return False
