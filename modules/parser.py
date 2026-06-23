# ---------------------------------------------------------------------------- #
#                                    Imports                                   #
# ---------------------------------------------------------------------------- #

from .tokens import TT, Token
import modules.ast_nodes as ast
from typing import Callable as callable

# ---------------------------------------------------------------------------- #
#                                    Parser                                    #
# ---------------------------------------------------------------------------- #

class ParserError(SyntaxError):
    ...

class Parser:
    def __init__(self, tokens: list[Token]):
        if not tokens:
            tokens = [Token(TT.EOF, None, -1, -1)]
        self.tokens = tokens
        self.pos = 0
        self.current = self.tokens[0]

        self.PRIMARY_HANDLERS: dict[TT, callable] = {
            TT.INT    : self._parse_number    ,
            TT.FLOAT  : self._parse_number    ,
            TT.BOOL   : self._parse_bool      ,
            TT.STR    : self._parse_string    ,
            TT.ID     : self._parse_identifier,
            TT.LPAREN : self._parse_grouping  ,
        }

        self.STATEMENT_HANDLERS: dict[TT, callable] = {
            TT.IF                 : self.parse_if       ,
            TT.DO                 : self.parse_while    ,
            TT.WHILE              : self.parse_while    ,
            TT.FOR                : self.parse_for      ,
            TT.FUNC               : self.parse_func_def ,
            TT.RIGHT_DOUBLE_ARROW : self.parse_return   ,
        }

        self.TYPE_HINT_TTs = (TT.INT_TYPE_HINT, 
                              TT.FLOAT_TYPE_HINT, 
                              TT.STR_TYPE_HINT, 
                              TT.BOOL_TYPE_HINT,
                              TT.NOTHING_TYPE_HINT)

    # ------------------------- pre-parsing variables ------------------------ #

    
    UNARY_OPS = (TT.NOT, TT.MINUS, TT.PLUS)

    POSTFIX_OPS = (TT.INCREMENT, TT.DECREMENT)

    BINARY_PRECEDENCE: dict[TT, int] = {
        TT.OR   : 1, TT.XOR: 1,
        TT.AND  : 2,
        TT.EQ   : 3, TT.NEQ:   3, TT.TYPE_EQ : 3, TT.TYPE_NEQ : 3,
        TT.LT   : 4, TT.GT   : 4, TT.LTE     : 4, TT.GTE      : 4,
        TT.PLUS : 5, TT.MINUS: 5,
        TT.STAR : 6, TT.SLASH: 6, TT.PERCENT : 6,
    }

    ASSIGN_OPS = (TT.ASSIGN, 
                  TT.PLUS_EQ, 
                  TT.MINUS_EQ, 
                  TT.STAR_EQ, 
                  TT.SLASH_EQ, 
                  TT.PERCENT_EQ, 
                  TT.AND_EQ, 
                  TT.OR_EQ, 
                  TT.XOR_EQ)

    # ---------------------------- helper methods ---------------------------- #

    def advance(self, steps: int =1):
        for _ in range(steps):
            self.pos += 1
            self.current = self.tokens[self.pos] if self.pos < len(self.tokens) else Token(TT.EOF, None, -1, -1)

    def peek(self, steps: int =1) -> Token | None:
        peek = self.pos + steps
        if peek >= len(self.tokens):
            return None
        return self.tokens[peek]
    
    def expect(self, token_type: TT):
        """consumes the current token if it matches the expected `token_type`,
        else raises a parse error"""
        if self.current.type != token_type:
            raise ParserError(f'Expected {token_type}, got {self.current.type} '
                              f'at {self.current.line}, {self.current.column}')
        token = self.current
        self.advance()
        return token
    
    def check(self, *token_types: TT) -> bool:
        return self.current.type in token_types
    
    def _consume_statement_terminator(self) -> None:
        """
        Semicolon rules after a statement:
        - Required in general (e.g. `x = 5` must be followed by `;`).
        - NOT required if the statement just parsed ended in '}' (e.g. an
          `if`/`while`/`for` block) - the brace is unambiguous on its own.
        - NOT required if we're now sitting on '}' or EOF - i.e. this was
          the last statement in a block, or the last statement in the file.
        """

        if self.check(TT.RBRACE, TT.EOF):
            if self.peek() == TT.SEMICOLON:
                self.expect(TT.SEMICOLON)
            return
        
        previous = self.peek(-1)
        if previous is not None and previous.type == TT.RBRACE:
            if self.check(TT.SEMICOLON):
                self.expect(TT.SEMICOLON)
            return
        
        self.expect(TT.SEMICOLON)
        
    # ------------------------------ entry point ----------------------------- #

    def parse(self) -> ast.ProgramNode:
        statements = []
        while not self.check(TT.EOF):
            statements.append(self.parse_statement())
            self._consume_statement_terminator()
        return ast.ProgramNode(statements)
    
    # ------------------------------ statements ------------------------------ #

    def parse_statement(self) -> ast.Node:
        if self.check(TT.ID) and (peek1 := self.peek()) is not None and peek1.type == TT.COLON:
            return self.parse_var_decl()

        handler = self.STATEMENT_HANDLERS.get(self.current.type)
        if handler is not None:
            return handler()

        return self.parse_expression()
    
    def parse_var_decl(self):
        name_token = self.expect(TT.ID)
        self.expect(TT.COLON)
        type_hint = self.current
        if type_hint.type not in self.TYPE_HINT_TTs:
            raise ParserError(f'Expected a type hint, but got a {type_hint.type} '
                              f'at {type_hint.line, type_hint.column}')
        self.advance()
        self.expect(TT.ASSIGN)
        value = self.parse_expression()
        return ast.VarDeclNode(name_token, type_hint, value)
    
    
    # ------------------------------ expressions ----------------------------- #

    def parse_expression(self) -> ast.Node:
        return self.parse_assignment()
    
    def parse_assignment(self):
        left = self.parse_binary()
        if self.check(*self.ASSIGN_OPS):
            if not isinstance(left, ast.IdNode):
                raise ParserError(f'Invalid assignment target: {left!r}')
            assign_token = self.current
            self.advance()
            right = self.parse_assignment()
            return ast.AssignNode(left.token, assign_token, right)
        return left
    
    def parse_binary(self, min_precedence: int =1):
        left = self.parse_unary()

        while True:
            precedence = self.BINARY_PRECEDENCE.get(self.current.type)
            if precedence is None or precedence < min_precedence:
                break
            op = self.current
            self.advance()
            right = self.parse_binary(precedence + 1)
            left = ast.BinOpNode(left, op, right)
        return left
    
    def parse_unary(self):
        if self.check(*self.UNARY_OPS):
            op = self.current
            self.advance()
            operand = self.parse_unary()
            return ast.UnaryOpNode(op, operand)
        return self.parse_postfix()
    
    def parse_postfix(self):
        node = self.parse_primary()
        while True:
            if self.check(*self.POSTFIX_OPS):
                op = self.current
                self.advance()
                node = ast.PostfixOpNode(node, op)
            elif self.check(TT.LPAREN):
                node = self.parse_call(node)
            else:
                break
        return node
    
    def parse_call(self, callee_node) -> ast.CallNode:
        if not isinstance(callee_node, ast.IdNode):
            raise ParserError(f'Cannot call non-identifier expression: {callee_node!r}')
        
        self.expect(TT.LPAREN)
        args = []
        if not self.check(TT.RPAREN):
            args.append(self.parse_expression())
            while self.check(TT.COMMA):
                self.advance()
                args.append(self.parse_expression())
        self.expect(TT.RPAREN)

        return ast.CallNode(callee_node.token, args)
    
    def parse_if(self) -> ast.IfNode:
        """
        if (cond) {...}
        else if (cond) {...} <- Zero or more else if blocks
        else {...} <- optional but must be last"""
        branches = []
        else_body = None

        self.expect(TT.IF)
        self.expect(TT.LPAREN)
        condition = self.parse_expression()
        self.expect(TT.RPAREN)
        body = self._parse_block()
        branches.append((condition, body))

        while self.check(TT.ELSE):
            self.advance()
            if self.check(TT.IF): # elif blocks
                self.advance()
                self.expect(TT.LPAREN)
                condition = self.parse_expression()
                self.expect(TT.RPAREN)
                body = self._parse_block()
                branches.append((condition, body))
            else:
                else_body = self._parse_block()
                break

        return ast.IfNode(branches, else_body)
    
    def parse_while(self) -> ast.WhileNode:
        """
        do {...}
        while (cond)

        OR

        while (cond) {
            ...}
        """
        is_do = self.check(TT.DO)
        if is_do:
            self.expect(TT.DO)
            body = self._parse_block()
            self.expect(TT.WHILE)
            self.expect(TT.LPAREN)
            condition = self.parse_expression()
            self.expect(TT.RPAREN)
            return ast.WhileNode(is_do, condition, body)
        self.expect(TT.WHILE)
        self.expect(TT.LPAREN)
        condition = self.parse_expression()
        self.expect(TT.RPAREN)
        body = self._parse_block()
        return ast.WhileNode(is_do, condition, body)
    
    def parse_for(self) -> ast.ForNode:
        """
        for (init; test; update) {
            ...}
        """
        self.expect(TT.FOR)
        self.expect(TT.LPAREN)
        init   = self.parse_statement()
        self.expect(TT.SEMICOLON)
        test   = self.parse_statement()
        self.expect(TT.SEMICOLON)
        update = self.parse_statement()
        self.expect(TT.RPAREN)
        body   = self._parse_block()
        return ast.ForNode(init, test, update, body)
    
    def parse_func_def(self) -> ast.FuncNode:
        self.expect(TT.FUNC)
        name = self.current
        self.advance()
        self.expect(TT.LPAREN)
        parameters = []
        if not self.check(TT.RPAREN):
            parameters.append(self._parse_param())
            while self.check(TT.COMMA):
                self.advance()
                parameters.append(self._parse_param())
        self.expect(TT.RPAREN)
        self.expect(TT.RIGHT_DOUBLE_ARROW)
        if not self.check(*self.TYPE_HINT_TTs):
            raise ParserError(f'Invalid return type hint in {name.value} function definition')
        return_type = self.current
        self.advance()
        body = self._parse_block()
        return ast.FuncNode(name.value, parameters, return_type, body)
    
    def _parse_param(self):
        param_name = self.expect(TT.ID)
        self.expect(TT.COLON)
        if not self.check(*self.TYPE_HINT_TTs):
            raise ParserError( f'Invalid parameter type hint at {self.current.line}:{self.current.column}')
        type_hint = self.current
        self.advance()
        return (param_name, type_hint)
    
    def parse_return(self):
        keyword = self.expect(TT.RIGHT_DOUBLE_ARROW)
        if self.check(TT.NOTHING_TYPE_HINT):
            return ast.ReturnNode(keyword, None)
        value = self.parse_expression()
        return ast.ReturnNode(keyword, value)
        
    def parse_primary(self):
        handler = self.PRIMARY_HANDLERS.get(self.current.type)
        if handler is None:
            raise ParserError(
                f'Unexpected token in expression: {self.current.type} '
                f'at {self.current.line}, {self.current.column}'
            )
        return handler()
    
    # --------------------------- primary handlers --------------------------- #
    
    def _parse_number(self):
        tok = self.current
        self.advance()
        return ast.NumberNode(tok.value, tok)
    
    def _parse_bool(self):
        tok = self.current
        self.advance()
        return ast.BoolNode(tok.value, tok)
    
    def _parse_string(self):
        tok = self.current
        self.advance()
        return ast.StringNode(tok.value, tok)
    
    def _parse_identifier(self):
        tok = self.current
        self.advance()
        return ast.IdNode(tok.value, tok)
    
    
    # ----------------------------- parse helpers ---------------------------- #
    def _parse_grouping(self):
        self.advance()
        expression = self.parse_expression()
        self.expect(TT.RPAREN)
        return expression
    
    def _parse_block(self):
        self.expect(TT.LBRACE)
        statements = []
        while not self.check(TT.RBRACE):
            if self.check(TT.EOF):
                raise ParserError(
                    f'Unterminated block, expected \'}}\' but reached end of input '
                    f'at {self.current.line},{self.current.column}'
                )
            statements.append(self.parse_statement())
            self._consume_statement_terminator()
        self.expect(TT.RBRACE)
        return statements
    
    
def parse(tokens: list[Token]) -> ast.ProgramNode:
    return Parser(tokens).parse()