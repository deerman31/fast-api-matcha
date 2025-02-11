import re


def is_pattern_match(s: str, pattern_str: str) -> bool:
    matches = re.findall(pattern_str, s)
    return len("".join(matches)) == len(s)


def length_check(v: str, min: int, max: int) -> bool:
    length = len(v)
    if length < min or length > max:
        return False
    return True
