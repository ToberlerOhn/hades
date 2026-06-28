

# ---------------------------------------------------------------------------- #
#                                    Imports                                   #
# ---------------------------------------------------------------------------- #

from dataclasses import dataclass
from typing import Any as any
from .tokens import Token, TT
from .scope import Scope
from .interpreter import InterpreterError

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
        target_name = self.target.value if hasattr(self.target, 'value') else self.target
        return f'AssignNode({target_name!r}, {self.assign_token.type}, {self.value!r})'

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
    
@dataclass
class ClassDefNode:
    name: str
    creator: FuncNode | None
    methods: list[FuncNode]
    overloads: list[FuncNode]

    def __repr__(self):
        return f'ClassDefNode({self.name}, creator={self.creator!r}, methods={self.methods!r}, overloads={self.overloads!r})'
    
@dataclass
class PropertyAccessNode:
    obj: any
    prop_name: Token

    def __repr__(self):
        return f'PropertyAccessNode({self.obj!r}.{self.prop_name.value})'
    
@dataclass
class PropertyAssignNode:
    obj: any
    prop_name: Token
    value: any

    def __repr__(self):
        return f'PropertyAccessNode({self.obj!r}.{self.prop_name.value} {self.value!r})'

# ---------------------------------------------------------------------------- #
#                                   Grouping                                   #
# ---------------------------------------------------------------------------- #

@dataclass
class ProgramNode:
    statements: list

    def __repr__(self):
        return f'ProgramNode({self.statements})'
    
# ---------------------------------------------------------------------------- #
#                                Runtime Objects                               #
# ---------------------------------------------------------------------------- #
# These are not technically ast nodes but for right now I don't really have a 
# better place to put them. Runtime objects encode the data about each object
# in the ast node that is defined such as a function definition => function
# calls, class definitions and method calls => classes and methods.

@dataclass
class HadesFunction:
    name: str
    parameters: list
    return_type: Token
    body: list
    closure_scope: Scope

class HadesClass:
    
    def __init__(self, name: str, creator: HadesFunction | None, methods: dict[str, HadesFunction]):
        self.name = name
        self.creator = creator
        self.methods = methods

    def __repr__(self):
        return f'<class \'{self.name}\'>'

class HadesInstance:
    def __init__(self, hades_class: HadesClass, properties: dict[str, any]):
        self.hades_class = hades_class
        self.properties = properties

    def get(self, name: Token):
        if name in self.properties:
            return self.properties[name.value]
        if name.value in self.hades_class.methods:
            return self.hades_class.methods[name.value]
        raise InterpreterError(f'\'{self.hades_class.name}\' has no attribute \'{name.value}\'', name)
    
    def set(self, name: Token, value: any):
        self.properties[name.value] = value
    
    def __repr__(self):
        return f'<Instance of \'{self.hades_class.name}\'>'