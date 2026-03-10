from sympy import symbols, diff, sympify


def solve_derivative(expression):

    x = symbols("x")

    try:
        # -----------------------------------------
        # Normalize expression from OCR / speech
        # -----------------------------------------

        expression = expression.replace("^", "**")
        expression = expression.replace(" ", "")

        # remove common words
        expression = expression.replace("dx", "")
        expression = expression.replace("d/dx", "")

        # -----------------------------------------
        # Convert to symbolic expression
        # -----------------------------------------

        expr = sympify(expression)

        result = diff(expr, x)

        return str(result)

    except Exception:

        return None