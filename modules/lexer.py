# ---------------------------------------------------------------------------- #
#                                    Imports                                   #
# ---------------------------------------------------------------------------- #
from tokens import TT, Token
from helpers import match

# ---------------------------------------------------------------------------- #
#                                  Main Class                                  #
# ---------------------------------------------------------------------------- #

class Lexer:

	# ----------------------------- helper functions ----------------------------- #
	
	def __init__(self, text: str) -> None:
		self.text = text
		self.pos = 0
		self.line = 0
		self.column = 1
		self.current = self.text[0] if self.text else None

	def RaiseError(self, message: str):
		raise SyntaxError(f'Lexer error at ({self.line}, {self.column}): {message}')

	def advance(self, steps: int =1) -> None:
		for i in range(steps):
			if self.current == '\n':
				self.line += 1
				self.column = 1
			else:
				self.column += 1
			self.pos += 1
			self.current = self.text[self.pos] if self.pos < len(self.text) else None

	def peek(self, steps: int =1) -> str | None:
		peek = self.pos + steps
		return self.text[peek] if (0 <= peek < len(self.text)) else None
	
	# ------------------------------ main functions ------------------------------ #

	def skip_whitespace(self) -> None:
		while self.current and self.current in ' \n\r\t':
			self.advance()

	def skip_comment(self) -> None:
		if self.current == '/' and self.peek() == '/':
			while self.current and self.current != '\n':
				self.advance()
			if self.current == '\n':
				self.advance()

	def read_number(self) -> Token:
		start_line, start_col = self.line, self.column
		num = ''
		type = TT.INT

		while self.current and match(self.current, r'[\d\.]'):
			if self.current == '.':
				if type == TT.INT:
					type = TT.FLOAT
				else:
					self.RaiseError('Invalid float')
			num += self.current
			self.advance()
		value = float(num) if type == TT.FLOAT else int(num)
		return Token(type, value, start_line, start_col)
	
	def read_str(self) -> Token:
		start_line, start_col = self.line, self.column
		str_str = ''
		self.advance()

		while self.current and self.current != "'":
			if self.current == '\\':
				self.advance()
				match self.current:
					case 'n':
						str_str += '\n'
					case 't':
						str_str += '\t'
					case '\\':
						str_str += '\\'
					case _:
						str_str += self.current
				self.advance()
			else:
				str_str += self.current
				self.advance()

		if self.current != "'":
			self.RaiseError('Unterminated string literal')
		
		self.advance()
		return Token(TT.STR, str_str, start_line, start_col)
	
	def read_id(self) -> Token:
		start_line, start_col = self.line, self.column
		id = ''

		while self.current and match(self.current, r'[\w]'):
			id += self.current
			self.advance()

		# * Update later 
		keywords: dict[str, TT] = {
			'TRUE' : TT.BOOL,
			'FALSE': TT.BOOL,
			'_b'   : TT.BOOL_TYPE_HINT,
			'int'  : TT.INT_TYPE_HINT,
			'str'  : TT.STR_TYPE_HINT,
			'float': TT.FLOAT_TYPE_HINT,
		}

		tokenType = keywords.get(id, TT.ID)
		if tokenType == TT.BOOL:
			value = (id == 'TRUE')
		else:
			value = id

		return Token(tokenType, value, start_line, start_col)
	
	def get_next_token(self) -> Token:
		while self.current:
			while True:
				before = self.pos
				self.skip_whitespace()
				self.skip_comment()
				if self.pos == before:
					break
			if not self.current:
				break
			start_line, start_col = self.line, self.column

			# skip whitespace and comments:
			self.skip_whitespace()
			self.skip_comment()

			if not self.current:
				break

			# if the current character is a digit, get number content
			if match(self.current, r'\d'):
				return self.read_number()
			
			# if the current is an apostrophe (start of string), get string content
			if self.current == "'":
				return self.read_str()
			
			if match(self.current, r'[A-Za-z\_]'):
				return self.read_id()
			
			# --------------------------- 3 character tokens -------------------------- #
			# TYPE_EQ (===), TYPE_NEQ (!==)

			if self.current == self.peek() == self.peek(2) == '=':
				self.advance(3)
				return Token(TT.TYPE_EQ, '===', start_line, start_col)
			
			if self.current == '!' and (self.peek() == self.peek(2) == '='):
				self.advance(3)
				return Token(TT.TYPE_NEQ, '!==', start_line, start_col)
			
			# --------------------------- 2 character tokens -------------------------- #
			# EQ (==), NEQ (!=), GTE (>=), LTE (<=), AND (&&), OR (||),
			# XOR (^^), INCREMENT (++), DECREMENT (--)

			if self.current == self.peek() == '=':
				self.advance(2)
				return Token(TT.EQ, '==', start_line, start_col)
			
			if self.current == '!' and self.peek() == '=':
				self.advance(2)
				return Token(TT.NEQ, '!=', start_line, start_col)
			
			if self.current == '>' and self.peek() == '=':
				self.advance(2)
				return Token(TT.GTE, '>=', start_line, start_col)
			
			if self.current == '<' and self.peek() == '=':
				self.advance(2)
				return Token(TT.LTE, '<=', start_line, start_col)
			
			if self.current == self.peek() == '&':
				self.advance(2)
				return Token(TT.AND, '&&', start_line, start_col)
			
			if self.current == self.peek() == '|':
				self.advance(2)
				return Token(TT.OR, '||', start_line, start_col)
			
			if self.current == self.peek() == '^':
				self.advance(2)
				return Token(TT.XOR, '^^', start_line, start_col)
			
			if self.current == self.peek() == '+':
				self.advance(2)
				return Token(TT.INCREMENT, '++', start_line, start_col)
			
			if self.current == self.peek() == '-':
				self.advance(2)
				return Token(TT.DECREMENT, '--', start_line, start_col)
			
			# --------------------------- 1 character tokens -------------------------- #

			SINGLE_CHAR_TOKENS: dict[str, TT] = {
				'>': TT.GT,
				'<': TT.LT,
				'+': TT.PLUS,
				'-': TT.MINUS,
				'*': TT.STAR,
				'/': TT.SLASH,
				'%': TT.PERCENT,
				'=': TT.ASSIGN,
				'(': TT.LPAREN,
				')': TT.RPAREN,
				';': TT.SEMICOLON,
				':': TT.COLON,
				'!': TT.NOT,
			}

			if self.current in SINGLE_CHAR_TOKENS:
				char = self.current
				self.advance()
				return Token(SINGLE_CHAR_TOKENS[char], char, start_line, start_col)
			
			self.RaiseError(f'Unexpected character: {self.current}')

		return Token(TT.EOF, None, self.line, self.column)
	
	def tokenize(self) -> list[Token]:
		tokens: list[Token] = []
		while True:
			token = self.get_next_token()
			tokens.append(token)
			if token.type == TT.EOF:
				break
		return tokens
	
	def pretty_print(self):
		text = self.tokenize()
		current_line = 1
		temp = ''
		for token in text:
			if token.line == current_line:
				temp += f'({str(token)[9:]}  '
			else:
				temp += ' NEWLINE'
				print(temp)
				current_line += 1
				temp = f'({str(token)[9:]}  '
			
	
if __name__ == '__main__':
	test = \
	'''
	//test
	x: int = 5
	y: float = 5.2
	2 + x * 2;
	(4 * 2.2 + y*3.3) && 0
	x++
	'''

	lexer = Lexer(test)
	lexer.pretty_print()