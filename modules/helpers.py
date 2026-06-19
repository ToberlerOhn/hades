import re
def match(string: str, pattern: str) -> bool:
    """

    Check whether `pattern` matches somewhere in `string`

    Args:
        string (str): the string to search within
        pattern (str): the regex pattern to search for

    Returns:
        bool: whether the pattern was found
    """    
    m = re.search(pattern, string)
    return bool(m)

if __name__ == '__main__':
    print(match(r'2', r'[\d]'))
    print(match(r'5', r'535'))
    print(match(r'5', r'[53]'))