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

def f_error(error_type: str, message: str, source_text: str, line: int, column: int) -> str:
    lines = source_text.split('\n')
    if line < 0 or line >= len(lines):
        return f'{error_type}: {message} (at line {line + 1}, col {column})'
    
    error_line = lines[line]
    pointer = ' ' * (column - 1) + '^'
    
    return (
f'''
-- {error_type} ------------------------
Error: {message}
Line {line + 1}:
    {error_line}
    {pointer}
----------------------------------------''')

if __name__ == '__main__':
    ...