# ---------------------------------------------------------------------------- #
#                                    Imports                                   #
# ---------------------------------------------------------------------------- #
from modules.tokens import TT, Token
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
		raise SyntaxError(f'Lexer error at {self.line}:{self.column}: {message}')

	def advance(self, steps: int =1) -> None:
		for i in range(steps):
			if self.current == '\n':
				self.line += 1
				self.column = 1
			else:
				self.col += 1
			self.pos += 1
			self.current = self.text[self.pos] if self.pos < len(self.text) else None

	def peek(self, steps: int =1) -> str | None:
		peek = self.pos + steps
		return self.text[peek] if (0 <= peek <= len(self.text)) else None
	
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
			'TRUE': TT.BOOL,
			'FALSE': TT.BOOL,
			'bool': TT.BOOL,
			'int': TT.INT,
			'float': TT.FLOAT,
			'str': TT.STR,
		}

		tokenType = keywords.get(id, TT.ID)
		if tokenType == TT.BOOL:
			value = (id == 'TRUE')
		else:
			value = id

		return Token(tokenType, value, start_line, start_col)
	
	def get_next_token(self) -> Token:
		while self.current:
			start_line, start_col = self.line, self.column

			# skip whitespace and comments:
			self.skip_whitespace()
			self.skip_comment()

			# if the current character is a digit, greedily consume characters to find the number
			if match(self.current, r'\d'):
				return self.read_number()
			
			# get string content
			if self.current == "'":
				return self.read_str()
			
			if match(self.current, r'[A-z\_]'):
				self.read_id()
			
			# -------------------------- 3 character matches -------------------------- #
			# TYPE_EQ (===), TYPE_NEQ (!==)

			if self.current == self.peek() == self.peek(2) == '=':
				self.advance(3)
				return Token(TT.TYPE_EQ, '===', start_line, start_col)
			
			if self.current == '!' and (self.peek() == self.peek(2) == '='):
				self.advance(3)