"""
Define token types and Token class
"""

# ---------------------------------------------------------------------------- #
#                                    Imports                                   #
# ---------------------------------------------------------------------------- #

from enum import Enum, auto
from dataclasses import dataclass
from typing import Any

# ---------------------------------------------------------------------------- #
#                                  Token Types                                 #
# ---------------------------------------------------------------------------- #

class TT(Enum):
	
	# ---------------------------------- ignored --------------------------------- #
	COMMENT    = auto() # \//...
	NEWLINE    = auto() # \n
	WHITESPACE = auto() # \t, \r

	# --------------------------------- literals --------------------------------- #
	FLOAT = auto() # \d+\.\d+
	INT   = auto() # \d+
	BOOL  = auto() # TRUE | FALSE
	STR   = auto()
	ID    = auto()

	# -------------------------------- comparisons ------------------------------- #
	TYPE_EQ  = auto() #  ===
	TYPE_NEQ = auto() # \!==
	EQ       = auto() #  ==
	NEQ      = auto() # \!= 
	GTE      = auto() # >=
	LTE      = auto() # <=
	GT       = auto() # >
	LT       = auto() # <

	# ----------------------------------- logic ---------------------------------- #
	AND = auto() # &&
	OR  = auto() # ||
	XOR = auto() # ^^
	NOT = auto() # \!

	# -------------------------------- arithmetic -------------------------------- #
	INCREMENT = auto() # ++
	DECREMENT = auto() # --
	PLUS      = auto() # +
	MINUS     = auto() # -
	STAR      = auto() #\*
	SLASH     = auto() #\/\/
	PERCENT   = auto() # %

	# --------------------------------- grouping --------------------------------- #
	LPAREN = auto() #(
	RPAREN = auto() #)

	EOF = auto()

# ---------------------------------------------------------------------------- #
#                                  Token Class                                 #
# ---------------------------------------------------------------------------- #

@dataclass
class Token:
	type: TT
	value: Any
	line: int
	column: int

	def __repr__(self):
		return f'Token({self.type}, {self.value!r}, {self.line}:{self.column})'
	