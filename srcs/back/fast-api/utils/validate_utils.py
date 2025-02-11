import re


def is_pattern_match(s: str, pattern_str: str) -> bool:
    matches = re.findall(pattern_str, s)
    return len("".join(matches)) == len(s)


# 引数のvalueのlengthが min <= value <= maxに収まっているかを調べる
def length_check(value: str, min_length: int, max_length: int) -> bool:
    length = len(value)
    if min_length <= length and max_length >= length:
        return True
    else:
        return False
