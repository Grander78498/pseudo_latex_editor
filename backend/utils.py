import re
from typing import Union
from difflib import ndiff

"""
Модуль сравнения латех формул
"""


class Node:
    """
    Класс узла дерева выражения
    """

    def __init__(self, value: str, left: 'Node' = None, right: 'Node' = None):
        self.value = value
        self.left = left
        self.right = right


def swap_children_recursive(node):
    """
    Приведение деревьев к одному виду
    """

    if node:
        if node.value == '+':
            if node.left.value < node.right.value:
                node.left, node.right = node.right, node.left  # Swap children
        swap_children_recursive(node.left)  # Recurse on left subtree
        swap_children_recursive(node.right)  # Recurse on right subtree
    return node


def traverse_tree(node):
    """
    Проход по дереву для получения списка вершин
    """

    data = []
    if node:
        data.append(node.value)
        if node.left:
            data += traverse_tree(node.left)
        if node.right:
            data += traverse_tree(node.right)
    return data


def color_diffrencies(tree1, tree2):
    """
    Добавление вершин с разницами деревьев
    """

    diff = ndiff(tree1, tree2)  # Compare word-by-word
    compared_tree = []
    for line in diff:
        if line.startswith("+") and line != '+':
            compared_tree.append(f"\\textcolor{{green}}{{{line[2:]}}}")  # Green for additions
        elif line.startswith("-") and line != '-':
            compared_tree.append(f"\\textcolor{{red}}{{{line[2:]}}}")  # Red for deletions
        else:
            compared_tree.append(line.strip())
    return compared_tree


def rebuild_tree_color(flat_list):
    """
    Построение латех строки по списку вершин дерева
    """

    operator_map = {
        '+': lambda a, b: f"{a} + {b}",
        '-': lambda a, b: f"{a} - {b}",
        '*': lambda a, b: f"{a} \\cdot {b}" if a.isdigit() or b.isdigit() else f"{a} {b}",
        '/': lambda a, b: f"{a} / {b}",
        '^': lambda a, b: f"{a} ^ {{{b}}}",
        '\\frac': lambda a, b: f"\\frac{{{a}}}{{{b}}}",
        '-u': lambda a: f"-{a}",
        '\sin': lambda a: f"\\sin{{({a})}}",
        '\cos': lambda a: f"\\cos{{({a})}}",
        '\tan': lambda a: f"\\tan{{({a})}}",
        '\log': lambda a: f"\\log{{({a})}}",
        '\sqrt': lambda a: f"\\sqrt{{({a})}}",
        '(': lambda a: f"({a})",
        '{': lambda a: f"{{{a}}}"
    }

    def helper(index, color=None):
        """
        Recursive helper function to rebuild the tree.
        :param index: Current index in the flat list.
        :return: A tuple (reconstructed subtree, next index to process).
        """

        token = flat_list[index]

        match = re.match(r'\\textcolor\s*{(\w+)}\s*{([^}]*)}', token)
        if match:
          color = match.group(1)
          token = match.group(2)


        if token in operator_map:  # If the token is an operator/function
            num_args = operator_map[token].__code__.co_argcount  # Get the required number of arguments
            next_index = index + 1
            if num_args == 1:  # Unary operator (e.g., sin, cos)
              child, next_index = helper(next_index)

              if color:
                return f'\\textcolor{{{color}}}{operator_map[token](child)}', next_index

              return operator_map[token](child), next_index

            elif num_args == 2:  # Binary operator (e.g., add, mul)
              child1, next_index = helper(next_index)
              child2, next_index = helper(next_index)

              if color:
                return f'{child1} \\textcolor{{{color}}}{{{token}}} {child2}', next_index

              return operator_map[token](child1, child2), next_index

        if color:
          return f'\\textcolor{{{color}}}{{{token}}}', index + 1

        return token, index + 1

    # Start the recursive rebuilding from the first element
    index = 0
    tree = ''
    while index != len(flat_list):
      new_tree, index = helper(index)
      tree += new_tree
    return tree


def tokenize(latex: str):
    """
    Токенизация латех строки
    """

    token_specification = [
        ('NUMBER', r'\d+(\.\d*)?'),  # Numbers (integers or decimals)
        ('FUNC', r'\\[a-zA-Z]+'),  # LaTeX functions like \sin, \cos
        ('VAR', r'[a-zA-Z]'),  # Variables (single letters)
        ('OP', r'[+\-*/^]'),  # Operators
        ('LPAREN', r'\('),  # Left parenthesis
        ('RPAREN', r'\)'),  # Right parenthesis
        ('LBRACE', r'\{'),  # Left curly brace
        ('RBRACE', r'\}'),  # Right curly brace
        ('SKIP', r'\s+'),  # Skip whitespace
        ('MISMATCH', r'.')  # Any other character (to catch errors)
    ]
    token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)

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
    Класс парсера для построения дерева выражения по строке
    """

    def __init__(self, tokens):
        self.tokens = list(tokens)
        self.pos = 0
        self.root = None

    def parse(self):
        self.root = self.expression()
        return self.root

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume(self):
        token = self.peek()
        self.pos += 1
        return token

    def expression(self):
        node = self.term()
        while self.peek() and self.peek()[1] in ('+', '-'):
            op = self.consume()[1]
            right = self.term()
            node = Node(op, node, right)
        return node

    def term(self):
        node = self.factor()
        while self.peek() and self.peek()[1] in ('*', '/'):
            op = self.consume()[1]
            right = self.factor()
            node = Node(op, node, right)
        return node

    def factor(self):
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
            func = self.consume()[1]
            arg = self.factor()
            return Node(func, arg)
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


def latex_to_traversed(latex):
    """
    Перевод латех строки в список вершин дерева выражения.
    """

    tokens = tokenize(latex)
    parser = LatexParser(tokens)
    tree = parser.parse()
    tree = swap_children_recursive(tree)
    return traverse_tree(tree)


def find_diffrencies(first_str, second_str):
    """
    Поиск различий между двумя латех формулами.
    Принимает две строки и возвращает латех строку.
    """

    tree1 = latex_to_traversed(first_str)
    tree2 = latex_to_traversed(second_str)

    res_diff = color_diffrencies(tree1, tree2)

    return rebuild_tree_color(res_diff)
