import re


def is_pattern_match(text: str, target_text: str) -> bool:
    match = re.fullmatch(target_text, text)
    return match is not None


# 引数のvalueのlengthが min <= value <= maxに収まっているかを調べる
def length_check(value: str, min_length: int, max_length: int) -> bool:
    return min_length <= len(value) <= max_length
