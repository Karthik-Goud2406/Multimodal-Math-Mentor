from utils.llm import call_llm


def route_problem(problem_text):

    prompt = f"""
Classify the math problem into:

algebra
probability
calculus
linear algebra

Problem:
{problem_text}

Return only topic.
"""

    topic = call_llm(prompt)

    return topic.strip()