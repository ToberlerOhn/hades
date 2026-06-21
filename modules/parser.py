# ---------------------------------------------------------------------------- #
#                                    Imports                                   #
# ---------------------------------------------------------------------------- #

from tokens import TT, Token
import ast_nodes as ast

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

        self.PRIMARY_HANDLERS = {
            TT.INT   : self._parse_number,
            TT.FLOAT : self._parse_number,
            TT.BOOL  : self._parse_bool,
            TT.STR   : self._parse_string,
            TT.ID    : self._parse_identifier,
            TT.LPAREN: self._parse_grouping,
        }

        self.STATEMENT_HANDLERS = {
            TT.IF: self.parse_if
        }

        self.TYPE_HINT_TTs = (TT.INT_TYPE_HINT, TT.FLOAT_TYPE_HINT, TT.STR_TYPE_HINT, TT.BOOL_TYPE_HINT)

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
            raise ParserError(f'Expected {token_type}, got {self.current.type}'
                              f'at {self.current.line}, {self.current.column}')
        token = self.current
        self.advance()
        return token
    
    def check(self, *token_types: TT) -> bool:
        return self.current.type in token_types
    
    # ------------------------------ entry point ----------------------------- #

    def parse(self) -> ast.ProgramNode:
        statements = []
        while not self.check(TT.EOF):
            statements.append(self.parse_statement())
            if self.check(TT.SEMICOLON):
                self.advance()
        return ast.ProgramNode(statements)
    
    # ------------------------------ statements ------------------------------ #

    def parse_statement(self):
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

    def parse_expression(self):
        return self.parse_assignment()
    
    def parse_assignment(self):
        left = self.parse_binary()
        if self.check(TT.ASSIGN):
            if not isinstance(left, ast.IdNode):
                raise ParserError(f'Invalid assignment target: {left!r}')
            self.advance()
            right = self.parse_assignment()
            return ast.AssignNode(left.token, right)
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
        
    
    def parse_call(self, callee_node): # VVV callee_node should be an IdNode
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
        if cond {...}
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
        statements = []
        self.expect(TT.LBRACE)
        while not self.check(TT.RBRACE):
            if self.check(TT.EOF):
                raise ParserError(
                    f'Unterminated block, expected \'}}\' but reached end of input '
                    f'at {self.current.line},{self.current.column}'
                )
            statements.append(self.parse_expression())
            if self.check(TT.SEMICOLON): self.advance()
        self.expect(TT.RBRACE)
        return statements
    
    
def parse(tokens: list[Token]) -> ast.ProgramNode:
    return Parser(tokens).parse()

# ---------------------------------------------------------------------------- #
#                                    Testing                                   #
# ---------------------------------------------------------------------------- #

if __name__ == '__main__':
    def tok(type_, value=None, line=1, col=1):
        return Token(type_, value, line, col)
    
    
    def run(name, tokens) -> ast.ProgramNode:
        print('\n' + '='*50)
        print(f'{name}')
        tokens = tokens + [tok(TT.EOF)]
        try:
            result = Parser(tokens).parse()
            print(result)
            return result
        except ParserError as e:
            print("ParseError:", e)
            return ast.ProgramNode([Token(TT.EOF, None, -1, -1)])
    
    # ------------------------------ basic tests ----------------------------- #
   
    run("2 + 3 * 2", [
        tok(TT.INT, 2), tok(TT.PLUS, '+'), tok(TT.INT, 3), tok(TT.STAR, '*'), tok(TT.INT, 2)
    ])
    
    run("a && b && c", [
        tok(TT.ID, 'a'), tok(TT.AND, '&&'),
        tok(TT.ID, 'b'), tok(TT.AND, '&&'),
        tok(TT.ID, 'c'),
    ])
    
    run("-5 + 3", [
        tok(TT.MINUS, '-'), tok(TT.INT, 5), tok(TT.PLUS, '+'), tok(TT.INT, 3)
    ])
    
    run("!TRUE && FALSE", [
        tok(TT.NOT, '!'), tok(TT.BOOL, True), tok(TT.AND, '&&'), tok(TT.BOOL, False)
    ])
    
    run("x = 5", [
        tok(TT.ID, 'x'), tok(TT.ASSIGN, '='), tok(TT.INT, 5)
    ])
    
    run("x = y = 5", [
        tok(TT.ID, 'x'), tok(TT.ASSIGN, '='),
        tok(TT.ID, 'y'), tok(TT.ASSIGN, '='),
        tok(TT.INT, 5)
    ])
    
    run("x: int = 5", [
        tok(TT.ID, 'x'), tok(TT.COLON, ':'), tok(TT.INT_TYPE_HINT, 'int'),
        tok(TT.ASSIGN, '='), tok(TT.INT, 5)
    ])
    
    run("(4 * 2.2 + y * 3.3) && 0", [
        tok(TT.LPAREN, '('),
        tok(TT.INT, 4), tok(TT.STAR, '*'), tok(TT.FLOAT, 2.2),
        tok(TT.PLUS, '+'),
        tok(TT.ID, 'y'), tok(TT.STAR, '*'), tok(TT.FLOAT, 3.3),
        tok(TT.RPAREN, ')'),
        tok(TT.AND, '&&'), tok(TT.INT, 0)
    ])
    
    run("x++", [
        tok(TT.ID, 'x'), tok(TT.INCREMENT, '++')
    ])
    
    run("//invalid target\n5 = 3", [
        tok(TT.INT, 5), tok(TT.ASSIGN, '='), tok(TT.INT, 3)
    ])
    
    run("2 + 3; x = 5", [
        tok(TT.INT, 2), tok(TT.PLUS, '+'), tok(TT.INT, 3), tok(TT.SEMICOLON, ';'),
        tok(TT.ID, 'x'), tok(TT.ASSIGN, '='), tok(TT.INT, 5)
    ])

    # ------------------------ test lexer with parser ------------------------ #

    from lexer import Lexer

    test = """
    x: int = 3;
    y: float = 3.5;
    z: float = 2 * x + y;
    // comment
    x && y || !TRUE;
    """

    l = Lexer(test)
    run(test, l.tokenize())