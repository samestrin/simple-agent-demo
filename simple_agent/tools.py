# tools.py

from langchain.tools import BaseTool
import wikipedia
import re
import ast
import operator
from typing import Dict, Any, Union, Type, Callable

class WikipediaTool(BaseTool):
    name: str = "wikipedia"
    description: str = "Useful for answering general knowledge questions. Input should be a single string; it returns the summary of the top page."

    def _run(self, query: str) -> str:
        """
        Searches Wikipedia for the given query and returns the first sentence of the summary.
        
        Args:
            query: The search term to look up on Wikipedia
            
        Returns:
            str: A two-sentence summary of the Wikipedia page or an error message
            
        Note:
            Uses wikipedia.summary() which may raise PageError, DisambiguationError,
            or HTTPTimeoutError in case of issues with the Wikipedia API.
        """
        try:
            # wikipedia.page() would give more details but might lead to disambiguation issues
            # Using summary directly with sentence limiting for conciseness
            summary = wikipedia.summary(query, sentences=2)
            return summary
        except Exception as e:
            return f"❗ Could not fetch Wikipedia page for '{query}'. Error: {e}"

class CalculatorTool(BaseTool):
    name: str = "calculator"
    description: str = "Useful for math questions. Input should be a valid math expression (e.g., 16 * 4 + 3). For square roots, use 'x ** 0.5' instead of 'sqrt(x)'. Do not use quotes around the expression."

    def _run(self, expression: str) -> str:
        """Evaluates a simple math expression and returns the result."""
        try:
            # Strip any quotes from the expression
            expression = expression.strip("'\"")
            
            # Check for common square root requests and convert them
            if "square root" in expression.lower() or "sqrt" in expression.lower():
                # Extract the number from expressions like "square root of 144" or "sqrt(144)"
                match = re.search(r'\d+', expression)
                if match:
                    number = int(match.group())
                    # Calculate square root using exponentiation
                    return str(number ** 0.5)
                else:
                    return "❗ Could not identify a number to calculate square root."
                    
            # Only allow digits, operators, parentheses, decimals, and spaces
            if not re.fullmatch(r"[0-9+\-*/().\s\*]+", expression):  # Added \* to allow ** operator
                return "❗ Invalid characters in expression."
            
            # Parse the expression into an AST
            node = ast.parse(expression, mode='eval')
            
            # Define allowed operators
            operators: Dict[Type[ast.operator], Callable] = {
                ast.Add: operator.add,
                ast.Sub: operator.sub,
                ast.Mult: operator.mul,
                ast.Div: operator.truediv,
                ast.USub: operator.neg,  # Unary minus
                ast.Pow: operator.pow,   # Add power operator for square roots
            }
            
            # Define a visitor to evaluate the expression safely
            def eval_expr(node: Any) -> Union[int, float]:
                """
                Recursively evaluates an AST node representing a mathematical expression.
                
                Args:
                    node: An AST node to evaluate
                    
                Returns:
                    Union[int, float]: The result of evaluating the expression
                    
                Raises:
                    ValueError: If the expression contains unsupported operations or node types
                """
                if isinstance(node, ast.Num):  # Simple number node
                    return node.n
                elif isinstance(node, ast.BinOp):  # Binary operation (e.g., a + b)
                    if type(node.op) not in operators:
                        raise ValueError(f"Unsupported operation: {type(node.op).__name__}")
                    return operators[type(node.op)](eval_expr(node.left), eval_expr(node.right))
                elif isinstance(node, ast.UnaryOp):  # Unary operation (e.g., -a)
                    if type(node.op) not in operators:
                        raise ValueError(f"Unsupported operation: {type(node.op).__name__}")
                    return operators[type(node.op)](eval_expr(node.operand))
                elif isinstance(node, ast.Expression):  # Root node of the expression
                    return eval_expr(node.body)
                else:
                    raise ValueError(f"Unsupported node type: {type(node).__name__}")
            
            result = eval_expr(node)
            return str(result)
        except Exception as e:
            return f"❗ Error evaluating expression: {e}"
