"""Entry point to running .hds files
Usage: python3 run_hds.py path_to_file.hds"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from modules.lexer import Lexer
from modules.parser import Parser
from modules.interpreter import Interpreter, InterpreterError

def main():
    if len(sys.argv) < 2:
        print('Usage: hds <file.hds>')
        sys.exit(1)

    file_path = Path(sys.argv[1])

    if not file_path.exists():
        print(f'Error: file path not found: {file_path}')
        sys.exit(1)
    
    if file_path.suffix not in ['.hd', '.hds']:
        print(f'Warning: expected a .hds file, got \'{file_path.suffix}\'')
    
    source = file_path.read_text()

    try:
        tokens = Lexer(source).tokenize()
        tree = Parser(tokens).parse()
        Interpreter().evaluate(tree)
    except (SyntaxError, InterpreterError) as e:
        print(f'Error: {e}')
        sys.exit(1)

if __name__ == "__main__":
    main()