

def parse_question(question):

    topic = "unknown"

    if "derivative" in question.lower():
        topic = "calculus"

    elif "probability" in question.lower():
        topic = "probability"

    elif "matrix" in question.lower():
        topic = "linear_algebra"

    return {
        "problem_text": question,
        "topic": topic,
        "variables": [],
        "constraints": [],
        "needs_clarification": False
     }