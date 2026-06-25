

# ---------------------------------------------------------------------------- #
#                                    Imports                                   #
# ---------------------------------------------------------------------------- #

from dataclasses import dataclass
from typing import Any as any
from .tokens import Token, TT
from .scope import Scope

type Node = (NumberNode | BoolNode | StringNode | ListNode | IndexNode | IdNode | NothingNode | \
BinOpNode | UnaryOpNode | PostfixOpNode | AssignNode | VarDeclNode | \
IfNode | WhileNode | ForNode | ForInNode | FuncNode | ReturnNode | CallNode |\
ProgramNode)

# ---------------------------------------------------------------------------- #
#                                   Literals                                   #
# ---------------------------------------------------------------------------- #

@dataclass
class NothingNode:
    token: Token

    def __repr__(self):
        return f'NothingNode()'

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
class ListNode:
    elements: list
    token: Token

    def __repr__(self):
        return f'ListNode({self.elements!r})'

@dataclass
class IndexNode:
    callee: any
    index: any
    token: Token

    def __repr__(self):
        return(f'ListCall({self.callee!r}[{self.index!r}])')

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
    target: any
    assign_token: Token
    value: any

    def __repr__(self):
        return f'AssignNode({self.target.value!r}, {self.assign_token.type}, {self.value!r})'

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
class WhileNode:
    is_do: bool
    condition: Node
    body: list[any]

    def __repr__(self):
        return f'WhileNode(do={self.is_do}, {self.condition!r}, {self.body!r})'

@dataclass
class ForNode:
    init: Node
    testExpression: Node
    updateStatement: Node
    body: list[any]

    def __repr__(self):
        return f'ForNode({self.init}, {self.testExpression}, {self.updateStatement}, body={self.body!r})'

@dataclass
class ForInNode:
    iterator: VarDeclNode
    iterable: Node
    body: list[any]

    def __repr__(self):
        return f'ForInNode({self.iterator!r}, {self.iterable!r}, body={self.body!r})'

# ---------------------------------------------------------------------------- #
#                                  Structures                                  #
# ---------------------------------------------------------------------------- #

@dataclass
class FuncNode:
    """Define a function"""
    name: str
    parameters: list[tuple[Token, Token]]
    return_type: Token
    body: list[any]

    def __repr__(self):
        return f'FuncDefNode({self.name}, {self.parameters!r} => {self.return_type}, body={self.body!r})'

@dataclass
class Function:
    name: str
    parameters: list
    return_type: Token
    body: list
    closure_scope: Scope

@dataclass
class ReturnNode:
    """`=> expr;` or `=> nothing;`"""
    keyword_token: Token
    value: any

    def __repr__(self):
        return f'ReturnNode({self.value!r})'

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