# ---------------------------------------------------------------------------- #
#                                    Imports                                   #
# ---------------------------------------------------------------------------- #

import ast_nodes as ast
from tokens import TT, Token
from scope import Scope
from typing import Any as any
from typing import Callable as callable


# ---------------------------------------------------------------------------- #
#                                Error Handling                                #
# ---------------------------------------------------------------------------- #

class InterpreterError(Exception):

    def __init__(self, message: str, token: Token | None = None):
        if token is not None:
            super().__init__(f'{message} at {token.line}, {token.column}')
        else:
            super().__init__(message)
        self.token = token

# ---------------------------------------------------------------------------- #
#                                  Interpreter                                 #
# ---------------------------------------------------------------------------- #

class Interpreter:

    def __init__(self):
        self.scope = Scope()

        self.NODE_HANDLERS: dict[any, callable] = {
            ast.ProgramNode  : self._eval_program,
            ast.NumberNode   : self._eval_number,
            ast.BoolNode     : self._eval_bool,
            ast.StringNode   : self._eval_string,
            ast.IdNode       : self._eval_id,
            ast.BinOpNode    : self._eval_binop,
            ast.UnaryOpNode  : self._eval_unaryop,
            ast.PostfixOpNode: self._eval_postfixop,
            ast.AssignNode   : self._eval_assign,
            ast.VarDeclNode  : self._eval_vardecl,
        }

        self.BINARY_OPS: dict[TT, callable] = {
            TT.PLUS    : lambda lhs, rhs:          lhs +         rhs,
            TT.MINUS   : lambda lhs, rhs:          lhs -         rhs,
            TT.STAR    : lambda lhs, rhs:          lhs *         rhs,
            TT.SLASH   : lambda lhs, rhs:          lhs /         rhs,
            TT.PERCENT : lambda lhs, rhs:          lhs %         rhs,
            TT.EQ      : lambda lhs, rhs:          lhs ==        rhs,
            TT.NEQ     : lambda lhs, rhs:          lhs !=        rhs,
            TT.TYPE_EQ : lambda lhs, rhs: type(    lhs) == type( rhs) and lhs == rhs,
            TT.TYPE_NEQ: lambda lhs, rhs: not(type(lhs) == type( rhs) and lhs == rhs),
            TT.LT      : lambda lhs, rhs:          lhs <         rhs,
            TT.GT      : lambda lhs, rhs:          lhs >         rhs,
            TT.LTE     : lambda lhs, rhs:          lhs <=        rhs,
            TT.GTE     : lambda lhs, rhs:          lhs >=        rhs,
            TT.AND     : lambda lhs, rhs: bool(    lhs) and bool(rhs),
            TT.OR      : lambda lhs, rhs: bool(    lhs) or bool( rhs),
            TT.XOR     : lambda lhs, rhs: (bool(   lhs) or bool( rhs)) and not(bool(lhs) and bool(rhs)) # (p V q) ^ ~(p ^ q) https://en.wikipedia.org/wiki/Exclusive_or#Definition
        }

        self.UNARY_OPS: dict[TT, callable] = {
            TT.MINUS : lambda o: -o,
            TT.PLUS  : lambda o: abs(o),
            TT.NOT   : lambda o: not bool(o)
        }

    # ------------------------------ entry point ----------------------------- #

    def evauluate(self, node):
        handler = self.NODE_HANDLERS.get(type(node))
        if handler is None:
            raise InterpreterError(f'No evaluator for node type: {type(node).__name__}')
        return handler(node)
    
    def _eval_program(self):
        ...
    
    def _eval_number(self):
        ...
    
    def _eval_bool(self):
        ...
    
    def _eval_string(self):
        ...
    
    def _eval_id(self):
        ...
    
    def _eval_binop(self):
        ...
    
    def _eval_unaryop(self):
        ...
    
    def _eval_postfixop(self):
        ...
    
    def _eval_assign(self):
        ...
    
    def _eval_vardecl(self):
        ...
    
        ...
    
