from utils.llm import call_llm
import json

def parse_question(question):

    prompt = f"""
Convert the following math problem into JSON. Extract the key elements.

Problem:
{question}

Return ONLY valid JSON with these exact keys:
"problem_text" (string): The cleaned up question.
"topic" (string): e.g. "calculus", "probability", "algebra", "linear_algebra"
"variables" (list of strings): Any variables present, e.g. ["x", "y"]
"constraints" (list of strings): Any limits or constraints mentioned.
"needs_clarification" (boolean): Set to true ONLY if the question is illegible, nonsense, or missing critical info to solve it.

JSON:
"""

    output = call_llm(prompt)
    output = output.strip()
    
    # Clean markdown if present
    if output.startswith("```json"):
        output = output.replace("```json", "", 1)
    if output.startswith("```"):
        output = output.replace("```", "", 1)
    if output.endswith("```"):
        output = output[:-3]

    try:
        parsed = json.loads(output.strip())
        # Ensure booleans are actually booleans
        if "needs_clarification" in parsed and str(parsed["needs_clarification"]).lower() == "true":
            parsed["needs_clarification"] = True
        else:
            parsed["needs_clarification"] = False
            
    except Exception as e:
        # Fallback if LLM fails JSON parsing
        parsed = {
            "problem_text": question,
            "topic": "unknown",
            "variables": [],
            "constraints": [],
            "needs_clarification": False
        }

    return parsed