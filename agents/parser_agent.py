
# from utils.llm import call_llm
# import json


# def parse_question(question):

#     prompt = f"""
# Convert this math problem into JSON:

# {question}

# Return fields:
# problem_text
# topic
# variables
# constraints
# needs_clarification
# """

#     output = call_llm(prompt)

#     try:
#         parsed = json.loads(output)
#     except:
#         parsed = {
#             "problem_text": question,
#             "topic": "unknown",
#             "variables": [],
#             "constraints": [],
#             "needs_clarification": True
#         }

#     return parsed


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