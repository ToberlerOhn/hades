

# ---------------------------------------------------------------------------- #
#                                    Imports                                   #
# ---------------------------------------------------------------------------- #

from dataclasses import dataclass
from typing import Any as any
from .tokens import Token

type Node = (NumberNode | BoolNode | StringNode | IdNode | \
BinOpNode | UnaryOpNode | PostfixOpNode | AssignNode | VarDeclNode | \
IfNode | CallNode |\
ProgramNode)

# ---------------------------------------------------------------------------- #
#                                   Literals                                   #
# ---------------------------------------------------------------------------- #

@dataclass
class NumberNode:
    value: any
    token: Token

    def __repr__(self):
        return f'NumberNode({self.value})'

@dataclass
class BoolNode:
    value: any
    token: Token

    def __repr__(self):
        return f'BoolNode({self.value})'

@dataclass
class StringNode:
    value: any
    token: Token

    def __repr__(self):
        return f'StringNode({self.value})'

@dataclass
class IdNode:
    value: any
    token: Token

    def __repr__(self):
        return f'IdNode({self.value})'
    
# ---------------------------------------------------------------------------- #
#                                  Operations                                  #
# ---------------------------------------------------------------------------- #

@dataclass
class BinOpNode:
    """Binary operations like arithmetic"""
    left: any
    op_token: Token
    right: any

    def __repr__(self):
        return f'BinOpNode({self.left!r}, {self.op_token.type}, {self.right!r})'
@dataclass
class UnaryOpNode:
    """Unary operations like negation"""
    op_token: Token
    operand: any

    def __repr__(self):
        return f'UnaryOpNode({self.op_token.type}, {self.operand!r})'
    
@dataclass
class PostfixOpNode:
    """Postfix operations like incrementation"""
    operand: any
    op_token: Token

    def __repr__(self):
        return f'PostfixOpNode({self.operand!r}, {self.op_token.type})'

@dataclass
class AssignNode:
    name_token: Token
    value: any

    def __repr__(self):
        return f'AssignNode({self.name_token.value!r} = {self.value!r})'
    
@dataclass
class VarDeclNode:
    name_token: Token
    type_hint: Token
    value: any

    def __repr__(self):
        return f'VarDeclNode({self.name_token.value!r}: {self.type_hint.type} = {self.value!r})'
    
# ---------------------------------------------------------------------------- #
#                                 Control Flow                                 #
# ---------------------------------------------------------------------------- #

@dataclass
class IfNode:
    branches: list[tuple[any, list]]
    else_body: list | None

    def __repr__(self):
        return f'IfNode(branches={self.branches!r}, else_body = {self.else_body!r})'

@dataclass
class CallNode:
    """Call a function"""
    callee_token: Token # the function being called
    args: list

    def __repr__(self):
        return f'CallNode({self.callee_token.value!r}, args={self.args!r})'

# ---------------------------------------------------------------------------- #
#                                   Grouping                                   #
# ---------------------------------------------------------------------------- #

@dataclass
class ProgramNode:
    statements: list

    def __repr__(self):
        return f'ProgramNode({self.statements})'