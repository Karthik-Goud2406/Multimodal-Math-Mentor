# from utils.llm import call_llm
# from tools.math_solver import solve_derivative
# from utils.llm import stream_llm
# def solve_problem(problem, retrieved_docs):

#     problem_lower = problem.lower()

#     # ----------------------------------------
#     # 1️⃣ Try symbolic math first (FAST)
#     # ----------------------------------------

#     if "derivative" in problem_lower:

#         try:

#             expression = problem_lower.split("of")[-1].strip()

#             symbolic_result = solve_derivative(expression)

#             if symbolic_result:
#                 return symbolic_result

#         except:
#             pass


#     # ----------------------------------------
#     # 2️⃣ Use only TOP context document
#     # ----------------------------------------

#     context = ""

#     if retrieved_docs:
#         context = str(retrieved_docs[0])


#     # ----------------------------------------
#     # 3️⃣ Smaller prompt for faster inference
#     # ----------------------------------------

#     prompt = f"""
# You are a math solver.

# Problem:
# {problem}

# Relevant rule:
# {context}

# Return ONLY the final answer.
# """


#     # ----------------------------------------
#     # 4️⃣ Call LLM
#     # ----------------------------------------

#     result = call_llm(prompt)

    
#     return stream_llm(prompt)
#     return f"{symbolic_result}"
    


from utils.llm import call_llm
from tools.math_solver import solve_derivative


def solve_problem(problem, retrieved_docs):

    problem_lower = problem.lower()

    # --------------------------------------------------
    # 1️⃣ Try symbolic math first (FAST)
    # --------------------------------------------------

    if "derivative" in problem_lower:

        try:
            expression = problem_lower.split("of")[-1].strip()

            symbolic_result = solve_derivative(expression)

            if symbolic_result:
                return str(symbolic_result)

        except Exception:
            pass

    # --------------------------------------------------
    # 2️⃣ Use top retrieved context
    # --------------------------------------------------

    context = ""

    if retrieved_docs:
        context = str(retrieved_docs[0])

    # --------------------------------------------------
    # 3️⃣ Small prompt for faster LLM inference
    # --------------------------------------------------

    prompt = f"""
You are a math solver.

Problem:
{problem}
git init
Relevant rule:
{context}

Return ONLY the final answer.
"""

    # --------------------------------------------------
    # 4️⃣ Call local LLM
    # --------------------------------------------------

    result = call_llm(prompt)

    return result