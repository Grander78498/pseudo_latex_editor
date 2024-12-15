import re
from difflib import ndiff
from .latex_parser import latex_to_traversed


"""
Module for analyzing latex strings.
"""


def find_diffrencies(tree1, tree2):
    """
    Finding diffrencies between two traversed equation trees

    :param tree1: Pre-ordered list of first tree's nodes
    :param tree2: Pre-ordered list of second tree's nodes
    :return: (Two pre-ordered lists of diffrences tree's nodes, simmilarity score)
    """

    score = 0
    total = 0
    diff = ndiff(tree1, tree2)  # Compare node-by-node
    first_tree = []  # Elements that are in the fisrt tree but not in the second
    second_tree = []  # Elements that are in the second tree but not in the first
    for line in diff:
        total += 1
        if line.startswith("+") and line != '+':
            score += 1
            second_tree.append(f"\\textcolor{{green}}{{{line[2:]}}}")
        elif line.startswith("-") and line != '-':
            score += 1
            first_tree.append(f"\\textcolor{{red}}{{{line[2:]}}}")
        else:
            first_tree.append(line.strip())
            second_tree.append(line.strip())
    return first_tree, second_tree, 1 - score / total


class PostfixToInfix:
    """
    Class for converting pre-ordered traversal list back into latex string.
    """

    # Operation priorities
    precedence = {
        '+': 1, '-': 1, '\\pm': 1,
        '*': 2, '/': 2,
        '^': 3
    }
    # Handled functions
    func = ['\\sin', '\\cos', '\\tan', '\\log', '\\sqrt', '#']

    def __init__(self):
        pass

    def postfix_to_infix(self, postfix):
        """
        Form a latex formula string based on a traversed equation tree
        :param postfix: Pre-ordered traversal list of equation tree
        :return: Latex string formula
        """
        stack = []
        i = len(postfix) - 1

        while i >= 0:
            token = postfix[i]
            clear_token = re.sub(r'\\textcolor\s*{\w+}\s*{([^}]*)}', r'\1', token)

            if clear_token not in self.precedence and clear_token not in self.func + ['\\frac']:  # Handling variables
                stack.append(token)
            elif clear_token in self.func:  # Handling functions such as sin
                arg = stack.pop()
                if clear_token == '#':
                    token = token.replace('#', '-')
                stack.append(f"{token}{{{arg}}}")
            elif clear_token == '\\frac':  # Handling 'frac' diffrently because of its formula structure
                left = stack.pop()
                right = stack.pop()
                result = f"\\frac{{{left}}}{{{right}}}"
                stack.append(result)
            else:  # Handling operators
                left = stack.pop()
                right = stack.pop()

                # Check if braces are needed
                left = self.braces(left, clear_token)
                right = self.braces(right, clear_token)

                result = f"{left} {token} {right}"
                stack.append(result)

            i -= 1

        return stack.pop()  # Only one equation left in the stack

    def braces(self, operand, parent_op):
        """
        Adds braces around operand if needed

        :param operand: Operand that needs to be wrapped up in braces
        :param parent_op: Parent node's operator
        :return: Operand
        """

        clear_operand = re.sub(r'\\textcolor\s*{\w+}\s*{([^}]*)}', r'\1', operand)
        if '(' in clear_operand or ')' in clear_operand:
            return operand

        # Getting operand's operator
        for op in self.precedence:
            if f" {op} " in clear_operand:  # Operator in subtree
                child_op = op
                if self.precedence[child_op] < self.precedence[parent_op]:
                    return f"({operand})"  # Braces are needed

        return operand


def traversed_to_latex(tree):
    """
    Converting traversed tree back into latex string

    :param tree: Pre-ordered list of equation tree's nodes
    :return: Latex string formula
    """
    converter = PostfixToInfix()
    latex = converter.postfix_to_infix(tree)
    return latex


def analyze(first_str, second_str):
    """
    Main function for comparing two latex strings

    :param first_str: First latex string formula
    :param second_str: Second latex string formula
    :return: Two latex strings showing diffrances between two formulas and simmilarity score
    """

    tree1 = latex_to_traversed(first_str)
    tree2 = latex_to_traversed(second_str)

    diff_tree1, diff_tree2, score = find_diffrencies(tree1, tree2)
    diff_str1, diff_str2 = traversed_to_latex(diff_tree1), traversed_to_latex(diff_tree2)

    return diff_str1, diff_str2, score
