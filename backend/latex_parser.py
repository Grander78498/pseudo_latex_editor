import re

"""
Module for parsing latex text formulas into equation trees.
"""


class Node:
    """
    Node of a binary equation tree.
    """

    def __init__(self, value: str, left: 'Node' = None, right: 'Node' = None):
        self.value = value
        self.left = left
        self.right = right


def tokenize(latex: str):
    """
    :param latex: text representation of a latex formula
    :return: generator containing tokens and token types
    """

    # Regular expressions to match operators, variables, numbers, functions, braces, etc.
    token_specification = [
        ('NUMBER', r'\d+(\.\d*)?'),  # Numbers (integers or decimals)
        ('FUNC', r'\\[a-zA-Z]+'),  # LaTeX functions like \sin, \cos
        ('VAR', r'[a-zA-Z]'),  # Variables (single letters)
        ('OP', r'[\+\-\*/\^]'),  # Operators
        ('LPAREN', r'\('),  # Left parenthesis
        ('RPAREN', r'\)'),  # Right parenthesis
        ('LBRACE', r'\{'),  # Left curly brace
        ('RBRACE', r'\}'),  # Right curly brace
        ('SKIP', r'\s+'),  # Skip whitespace
        ('MISMATCH', r'.')  # Any other character (to catch errors)
    ]

    token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)
    # Check all found tokens
    for match in re.finditer(token_regex, latex):
        kind = match.lastgroup
        value = match.group()
        if kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise SyntaxError(f"Unexpected character: {value}")
        yield kind, value


class LatexParser:
    """
    Class for parsing latex string into an equation trees.
    Handles functions such as \\sin, \\cos, \\tan, \\log, \\sqrt,
    \\frac, ^, +, -, *
    special letters such as \alpha, \beta, numbers and variables
    """

    def __init__(self, tokens):
        self.tokens = list(tokens)
        self.pos = 0  # Current position for analyzing token list
        self.root = None

    def parse(self):
        """
        Parses the token list into an equation tree and stores the root.
        """
        self.root = self.expression()
        return self.root

    def peek(self):
        """
        Checks next token
        :return: (token type, token value)
        """
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume(self):
        """
        Transmits to next token
        :return: (token type, token value)
        """
        token = self.peek()
        self.pos += 1
        return token

    def expression(self):
        """
        Handles addition and subtraction
        """
        node = self.term()
        while self.peek() and self.peek()[1] in ('+', '-'):
            op = self.consume()[1]
            right = self.term()
            node = Node(op, node, right)
        return node

    def term(self):
        """
        Handles multiplication, exponentiation and division
        """
        node = self.factor()
        while self.peek() and self.peek()[1] in ('*', '/', '^'):
            op = self.consume()[1]
            right = self.factor()
            node = Node(op, node, right)
        return node

    def factor(self):
        """
        Handles functions, variables, numbers, and parenthesis
        """
        token = self.peek()
        if token is None:
            raise SyntaxError("Unexpected end of input")

        kind, value = token
        if kind == 'NUMBER' or kind == 'VAR':
            self.consume()
            return Node(value)

        elif kind == 'FUNC' and value == '\\frac':
            self.consume()
            if self.peek() and self.peek()[0] == 'LBRACE':
                self.consume()
                numerator = self.expression()
                if self.peek() and self.peek()[0] == 'RBRACE':
                    self.consume()
                else:
                    raise SyntaxError("Missing closing brace for numerator in \\frac")

                if self.peek() and self.peek()[0] == 'LBRACE':
                    self.consume()
                    denominator = self.expression()
                    if self.peek() and self.peek()[0] == 'RBRACE':
                        self.consume()
                    else:
                        raise SyntaxError("Missing closing brace for denominator in \\frac")
                    return Node('\\frac', numerator, denominator)
                else:
                    raise SyntaxError("Missing denominator for \\frac")

        elif kind == 'FUNC':
            if value in ['\\sin', '\\cos', '\\tan', '\\log', '\\sqrt']:
                func = self.consume()[1]
                arg = self.factor()
                return Node(func, arg)
            else:  # This is a letter such as '\\alpha', it can be considered as a leaf
                self.consume()
                return Node(value)

        elif kind == 'LPAREN':
            self.consume()
            node = self.expression()
            if self.peek() and self.peek()[0] == 'RPAREN':
                self.consume()
                return node
            else:
                raise SyntaxError("Missing closing parenthesis")

        elif kind == 'LBRACE':
            self.consume()
            node = self.expression()
            if self.peek() and self.peek()[0] == 'RBRACE':
                self.consume()
                return node
            else:
                raise SyntaxError("Missing closing brace")

        elif kind == 'OP' and value == '-':
            self.consume()
            node = self.factor()
            return Node('-', None, node)

        else:
            raise SyntaxError(f"Unexpected token: {value}")


def swap_children_recursive(node):
    """
    Bringing children of '+' and '*' nodes to lexicographical order.

    :param node: Root of equation tree
    :return: Root of changed equation tree
    """

    if node:
        if node.value == '+' or node.value == '*':
            if node.left.value < node.right.value:
                node.left, node.right = node.right, node.left  # Swap children
        # Recurse on subtrees
        swap_children_recursive(node.left)
        swap_children_recursive(node.right)
    return node


def traverse_tree(node):
    """
    Pre-oder tree traversal

    :param node: Root of equation tree
    :return: Pre-ordered list of tree's nodes
    """

    data = []
    if node:
        data.append(node.value)
        if node.left:
            data += traverse_tree(node.left)
        if node.right:
            data += traverse_tree(node.right)
    return data


def latex_to_traversed(latex):
    """
    Converting latex string into a list of equation tree's nodes

    :param latex: text representation of a latex formula
    :return: pre-ordered list of built equation tree's nodes
    """

    tokens = tokenize(latex)
    parser = LatexParser(tokens)
    tree = parser.parse()
    tree = swap_children_recursive(tree)
    return traverse_tree(tree)
