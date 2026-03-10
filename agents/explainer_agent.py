from utils.llm import call_llm

def explain_solution(problem, solution, context):

    prompt = f"""
Explain the solution step-by-step for a student.

Problem:
{problem}

Final Answer:
{solution}

Helpful rules:
{context}

Explain clearly.
"""

    explanation = call_llm(prompt)

    return explanation

