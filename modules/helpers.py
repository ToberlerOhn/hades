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
    pointer = ' ' * (column - 1) + '\033[31m^\033[0m' # red arrow
    
    return (
f'''
-- {error_type} ------------------------
\033[1;31mError: {message}\033[0m
Line {line + 1}:
      \033[4m{error_line}\033[0m
      {pointer}
----------------------------------------''')

if __name__ == '__main__':
    # gap = 26
    # for r in range(0, 256, gap):
    #     for g in range(0, 256, gap):
    #         for b in range(0, 256, gap):
    #             print(f'\033[38;2;{r};{g};{b}m rgb({r}, {g}, {b})\033[0m')
    for i in range(30, 37 + 1):
        print("\033[%dm%d\t\t\033[%dm%d" % (i, i, i + 60, i + 60))

    print("\\033[39m\\033[49m                 - Reset color")
    print("\\033[2K                          - Clear Line")
    print("\\033[<L>;<C>H or \\033[<L>;<C>f   - Put the cursor at line L and column C.")
    print("\\033[<N>A                        - Move the cursor up N lines")
    print("\\033[<N>B                        - Move the cursor down N lines")
    print("\\033[<N>C                        - Move the cursor forward N columns")
    print("\\033[<N>D                        - Move the cursor backward N columns\n")
    print("\\033[2J                          - Clear the screen, move to (0,0)")
    print("\\033[K                           - Erase to end of line")
    print("\\033[s                           - Save cursor position")
    print("\\033[u                           - Restore cursor position\n")
    print("\\033[4m                          - Underline on")
    print("\\033[24m                         - Underline off\n")
    print("\\033[1m                          - Bold on")
    print("\\033[21m                         - Bold off")