# ---------------------------------------------------------------------------- #
#                                    Imports                                   #
# ---------------------------------------------------------------------------- #

import modules.ast_nodes as ast
from .tokens import TT, Token
from .scope import Scope
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
            ast.CallNode     : self._eval_call,
            ast.IfNode       : self._eval_if,
            ast.WhileNode    : self._eval_while,
            ast.ForNode      : self._eval_for,
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

        self.POSTFIX_OPS: dict[TT, callable] = {
            TT.INCREMENT: lambda o: o + 1,
            TT.DECREMENT: lambda o: o - 1
        }

        self.ASSIGN_OPS: dict[TT, callable] = {
            TT.ASSIGN    : lambda lhs, rhs:                    rhs,
            TT.PLUS_EQ   : lambda lhs, rhs: lhs +              rhs,
            TT.MINUS_EQ  : lambda lhs, rhs: lhs -              rhs,
            TT.STAR_EQ   : lambda lhs, rhs: lhs *              rhs,
            TT.SLASH_EQ  : lambda lhs, rhs: lhs /              rhs,
            TT.PERCENT_EQ: lambda lhs, rhs: lhs %              rhs,
            TT.AND_EQ    : lambda lhs, rhs: bool(lhs) & bool(  rhs),
            TT.OR_EQ     : lambda lhs, rhs: bool( lhs) | bool( rhs),
            TT.XOR_EQ    : lambda lhs, rhs: bool(lhs) ^ bool(  rhs)
        }

        self.BUILTINS: dict[str, callable] = {
            'print' : self.__print__   ,
            'type'  : self.__get_type__,
        }

    # ------------------------------ entry point ----------------------------- #

    def evaluate(self, node):
        handler = self.NODE_HANDLERS.get(type(node))
        if handler is None:
            raise InterpreterError(f'No evaluator for node type: {type(node).__name__}')
        return handler(node)

    # ------------------------------ statements ------------------------------ #

    def _eval_program(self, node: ast.ProgramNode):
        result = None
        for statement in node.statements:
            result = self.evaluate(statement)
        return result
        
    def _eval_vardecl(self, node: ast.VarDeclNode):
        value = self.evaluate(node.value)
        self._check_type_hint(value, node.type_hint, node.name_token)
        self.scope.declare(node.name_token.value, value)
        return value
    
    def _eval_assign(self, node: ast.AssignNode):
        rhs_value = self.evaluate(node.value)

        func = self.ASSIGN_OPS.get(node.assign_token.type)
        if func is None:
            raise InterpreterError(f'Unknown assigner \'{node.assign_token.value}\'')
        try:
            current_value = self.scope.get(node.name_token.value)
        except KeyError:
            raise InterpreterError(f'Cannot assign to undeclared variable \'{node.name_token.value}\'', node.name_token)
        
        try:
            new_value = func(current_value, rhs_value)
        except TypeError as e:
            raise InterpreterError(f'Invalid operand types for {node.assign_token.type.name}: '
                                   f'{type(current_value).__name__} and {type(rhs_value).__name__}',
                                   node.assign_token) from e
        
        self.scope.set(node.name_token.value, new_value)
        return new_value
    
    def _eval_if(self, node: ast.IfNode):
        for condition, body in node.branches:
            if self._truthy(self.evaluate(condition)):
                return self._eval_block(body)
        if node.else_body is not None:
            return self._eval_block(node.else_body)
        return None
    
    def _eval_while(self, node: ast.WhileNode):
        is_do = node.is_do
        condition, body = node.condition, node.body
        result = None
        if is_do:
            result = self._eval_block(body)
        while self._truthy(self.evaluate(condition)):
            result = self._eval_block(body)
        return result
    
    def _eval_for(self, node: ast.ForNode):
        init, test, update, body = node.init, node.testExpression, node.updateStatement, node.body
        result = self.evaluate(init)
        while self._truthy(self.evaluate(test)):
            result = self._eval_block(body)
            self.evaluate(update)
        return result

    def _eval_statements(self, statements: list):
        result = None
        for statement in statements:
            result = self.evaluate(statement)
        return result
    
    def _eval_call(self, node: ast.CallNode):
        name = node.callee_token.value
        func = self.BUILTINS.get(name)
        if func is None:
            raise InterpreterError(f'Undefined function \'{name}\'', node.callee_token)
        
        args = [self.evaluate(arg) for arg in node.args]
        return func(args, node.callee_token)
    
    # ------------------------------- literals ------------------------------- #
    
    def _eval_number(self, node: ast.NumberNode):
        return node.value
    
    def _eval_bool(self, node: ast.BoolNode):
        return node.value
    
    def _eval_string(self, node: ast.StringNode):
        return node.value
    
    def _eval_id(self, node: ast.IdNode):
        try:
            return self.scope.get(node.value)
        except KeyError:
            raise InterpreterError(f'Undefined variable \'{node.value}\'', node.token)

    # ------------------------------ operations ------------------------------ #

    def _eval_binop(self, node: ast.BinOpNode):
        left = self.evaluate(node.left)
        right = self.evaluate(node.right)
        op_type = node.op_token.type

        func = self.BINARY_OPS.get(op_type)
        if func is None:
            raise InterpreterError(f'Unknown binary operator: {op_type}', node.op_token)
        
        try:
            return func(left, right)
        except ZeroDivisionError:
            raise InterpreterError(f'Division by zero', node.op_token)
        except TypeError as e:
            raise InterpreterError(
                f'Invalid operand types for {op_type.name}: {type(left).__name__} and {type(right).__name__}', 
                node.op_token) from e
        
    def _eval_unaryop(self, node: ast.UnaryOpNode):
        value = self.evaluate(node.operand)
        op_type = node.op_token.type

        func = self.UNARY_OPS.get(op_type)
        if func is None:
            raise InterpreterError(f'Unknown unary operator: {op_type}', node.op_token)
        
        try:
            return func(value)
        except TypeError as e:
            raise InterpreterError(
                f"Invalid operand type for {op_type.name}: {type(value).__name__}",
                node.op_token,
            ) from e

    def _eval_postfixop(self, node: ast.PostfixOpNode):
        if not isinstance(node.operand, ast.IdNode):
            raise InterpreterError(
                f'Invalid target for {node.op_token.type.name}: {node.operand!r}',
                node.op_token
            )
        
        name = node.operand.value
        op_type = node.op_token.type
        try:
            old_value = self.scope.get(name)
        except KeyError:
            raise InterpreterError(f'Undefined variable: \'{name}\'', node.operand.token)
        
        func = self.POSTFIX_OPS.get(op_type)
        if func is None:
            raise InterpreterError(f'Unknown postfix operator: \'{op_type}\'', node.op_token)
        new_value = func(old_value)

        self.scope.set(name, new_value)
        return old_value
    
    # ------------------------------- built-ins ------------------------------ #

    def __print__(self, args: list, call_token: Token):
        print(*(self._to_string(a) for a in args))
        return None
    
    def __get_type__(self, args: list, call_token: Token):
        if len(args) != 1:
            raise InterpreterError(f'type() takes exactly 1 argument, but got {len(args)}', call_token)
        return self._python_type_to_hds_name(type(args[0]))
    
    @staticmethod
    def _python_type_to_hds_name(py_type):
        return {
            bool : 'bool' ,
            int  : 'int'  ,
            float: 'float',
            str  : 'str'  ,
        }.get(py_type, py_type.__name__)

    
    @staticmethod
    def _to_string(value) -> str:
        if isinstance(value, bool):
            return 'TRUE' if value else 'FALSE'
        if value is None:
            return 'nothing'
        if isinstance(value, float):
            return f'{value:.10g}'.rstrip('0').rstrip('.') if '.' in f'{value:.10g}' else f'{value:.10g}'
        return str(value)
    
    # --------------------------- helper functions --------------------------- #

    def _eval_block(self, statements: list):
        previous_scope = self.scope
        self.scope = Scope(previous_scope)
        try:
            return self._eval_statements(statements)
        finally:
            self.scope = previous_scope

    @staticmethod
    def _truthy(value) -> bool:
        if value is None:
            return False
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return value != 0
        if isinstance(value, str):
            return value != ''
        return bool(value)

    def _check_type_hint(self, value, type_hint_token: Token, name_token: Token):
        expected = {
            TT.INT_TYPE_HINT  : int,
            TT.FLOAT_TYPE_HINT: float,
            TT.BOOL_TYPE_HINT : bool,
            TT.STR_TYPE_HINT  : str,
        }.get(type_hint_token.type)

        if expected is None:
            return
        
        if expected is bool and not isinstance(value, bool):
            raise InterpreterError(
                f'Type mismatch for \'{name_token.value}\': expected bool, but got {type(value).__name__}',
                name_token
            )
        if expected is not bool and not isinstance(value, expected):
            raise InterpreterError(
                f'Type mismatch for \'{name_token.value}\': expected {expected.__name__}, but got {type(value).__name__}',
                name_token
            )
    
def interpret_program(tree: ast.ProgramNode):
    return Interpreter().evaluate(tree)