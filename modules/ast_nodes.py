

# ---------------------------------------------------------------------------- #
#                                    Imports                                   #
# ---------------------------------------------------------------------------- #

from dataclasses import dataclass
from typing import Any
from tokens import Token

# ---------------------------------------------------------------------------- #
#                                   Literals                                   #
# ---------------------------------------------------------------------------- #

@dataclass
class NumberNode:
    value: Any
    token: Token

    def __repr__(self):
        return f'NumberNode({self.value})'

@dataclass
class BoolNode:
    value: Any
    token: Token

    def __repr__(self):
        return f'BoolNode({self.value})'

@dataclass
class StringNode:
    value: Any
    token: Token

    def __repr__(self):
        return f'StringNode({self.value})'

@dataclass
class IdNode:
    value: Any
    token: Token

    def __repr__(self):
        return f'IdNode({self.value})'
    
# ---------------------------------------------------------------------------- #
#                                  Operations                                  #
# ---------------------------------------------------------------------------- #

@dataclass
class BinOpNode:
    """Binary operations like arithmetic"""
    left: Any
    op_token: Token
    right: Any

    def __repr__(self):
        return f'BinOpNode({self.left!r}, {self.op_token.type}, {self.right!r})'
@dataclass
class UnaryOpNode:
    """Unary operations like negation"""
    op_token: Token
    operand: Any

    def __repr__(self):
        return f'UnaryOpNode({self.op_token.type}, {self.operand!r})'
    
@dataclass
class PostfixOpNode:
    """Postfix operations like incrementation"""
    operand: Any
    op_token: Token

    def __repr__(self):
        return f'PostfixOpNode({self.operand!r}, {self.op_token.type})'

@dataclass
class AssignNode:
    name_token: Token
    value: Any

    def __repr__(self):
        return f'AssignNode({self.name_token.value!r} = {self.value!r})'
    
@dataclass
class VarDeclNode:
    name_token: Token
    type_hint: Token
    value: Any

    def __repr__(self):
        return f'VarDeclNode({self.name_token.value!r}: {self.type_hint.type} = {self.value!r})'


# ---------------------------------------------------------------------------- #
#                                   Grouping                                   #
# ---------------------------------------------------------------------------- #

@dataclass
class ProgramNode:
    statements: list

    def __repr__(self):
        return f'ProgramNode({self.statements})'