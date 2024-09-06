import re


def extract_substrings(input_string):
    # 使用正则表达式匹配用 {} 包围的子字符串
    pattern = r'\{(.*?)\}'
    matches = re.findall(pattern, input_string)
    return matches