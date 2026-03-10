from utils.llm import call_llm

def verify_solution(problem, solution):

    prompt = f"""
You are a math solution verifier.

Check whether the solution to the math problem is correct.

Problem:
{problem}

Proposed Solution:
{solution}

Respond with:

correct
incorrect
or unsure

Also explain briefly if incorrect.
"""

    result = call_llm(prompt)

    return result