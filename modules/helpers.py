import re
def match(string: str, pattern: str) -> bool:
    """_summary_

    Args:
        string (str): the string you want to check for
        pattern (str): the regex pattern to search in (or any string really)

    Returns:
        bool: whether the string is in the pattern or not
    """    
    m = re.match(pattern, string)
    return bool(m)

if __name__ == '__main__':
    ...