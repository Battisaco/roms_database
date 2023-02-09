def str_to_int(s: str) -> int:
    """Converts a string to an integer."""
    return int(s.strip().replace(",", ""))


def str_to_float(s: str) -> float:
    """Converts a string to a float."""
    return float(s.strip())
