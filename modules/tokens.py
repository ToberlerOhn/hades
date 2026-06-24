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

	# --------------------------- variable type hints --------------------------- #

	FLOAT_TYPE_HINT   = auto() # float
	INT_TYPE_HINT     = auto() # int
	BOOL_TYPE_HINT    = auto() # bool
	STR_TYPE_HINT     = auto() # str
	NOTHING_TYPE_HINT = auto() # nothing
	LIST_TYPE_HINT    = auto() # list

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

	# assignment operators

	ASSIGN     = auto() #   =
	PLUS_EQ    = auto() #   +=
	MINUS_EQ   = auto() #   -=
	STAR_EQ    = auto() # \ *=
	SLASH_EQ   = auto() #   /=
	PERCENT_EQ = auto() #   %=
	AND_EQ     = auto() #   &&=
	OR_EQ      = auto() #   ||=
	XOR_EQ     = auto() #   ^^=

	# --------------------------------- grouping --------------------------------- #
	LPAREN   = auto() # (
	RPAREN   = auto() # )
	LBRACE   = auto() # {
	RBRACE   = auto() # }
	LBRACKET = auto() # [
	RBRACKET = auto() # ]

	# ------------------------------- punctuation ------------------------------- #
	SEMICOLON = auto() # ;
	COLON     = auto() # :
	COMMA     = auto() # ,

	# ------------------------------ other symbols ------------------------------ #
	RIGHT_ARROW        = auto() # ->
	RIGHT_DOUBLE_ARROW = auto() # =>

	# --------------------------------- keywords -------------------------------- #
	IF    = auto() # if
	ELSE  = auto() # else
	DO    = auto() # do
	WHILE = auto() # while
	FOR   = auto() # for
	FUNC  = auto() # func

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
