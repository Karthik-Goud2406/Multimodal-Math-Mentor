# Multimodal Math Mentor

AI-powered **Multimodal Math Problem Solver** built using a **Multi-Agent Architecture** that can understand and solve mathematical problems from **text, images, and audio inputs**, providing clear **step-by-step explanations**.

---

# Live Demo

Experience the application here:

**Live Application:**
https://multimodal-math-mentor-karthik.streamlit.app/

No installation required — open the link and start solving math problems instantly.

---

# Problem Statement

Traditional math-solving tools typically rely on **single input formats** such as typed equations. However, real-world users often interact with problems in multiple ways:

* Students write **handwritten equations**
* Teachers share **images of problems**
* Learners ask questions **verbally**
* Many AI tools provide **answers without explanation**

Existing systems also rely on **single large models**, which can reduce reliability and make reasoning less transparent.

This creates several challenges:

* Lack of **multimodal input support**
* Limited **explainability in AI-generated solutions**
* No **verification layer for correctness**
* Difficulty handling **complex mathematical reasoning**

---

# Proposed Solution

Multimodal Math Mentor solves these problems by combining **multimodal input processing** with a **multi-agent AI architecture**.

Users can submit math problems through:

* Text
* Image upload
* Audio input

The system processes the input and routes it through specialized agents responsible for understanding, solving, verifying, and explaining the problem.

This modular architecture improves:

* Accuracy
* Transparency
* Flexibility
* Learning support

---

# Key Features

Multimodal Input Support
Accepts math problems through text, images, or audio.

OCR Integration
Extracts mathematical expressions from uploaded images.

Speech-to-Text Processing
Converts spoken math questions into text queries.

Multi-Agent Reasoning Pipeline
Different AI agents collaborate to solve problems.

Retrieval-Augmented Generation (RAG)
Retrieves relevant mathematical knowledge during reasoning.

Solution Verification
Ensures generated answers are logically correct.

Step-by-Step Explanations
Helps users understand how the solution is derived.

Memory System
Stores previous interactions and solutions.

Interactive Web Interface
Built with Streamlit for a smooth user experience.

---

# System Architecture

The application uses a **multi-agent pipeline**, where each agent performs a specialized task.

### Agents

Parser Agent
Interprets and structures the mathematical problem.

Router Agent
Identifies the type of mathematical problem and selects the solving strategy.

Retriever Agent
Fetches relevant knowledge using Retrieval-Augmented Generation.

Solver Agent
Computes the mathematical solution.

Verifier Agent
Checks the correctness of the generated answer.

Explainer Agent
Produces step-by-step explanations.

Memory Manager
Stores past problem-solving interactions.

---

# Input Modes

Users can interact with the system through multiple input formats.

Text Input
Users type a math question directly into the interface.

Image Input
Users upload an image containing a math problem, and OCR extracts the equation.

Audio Input
Users speak the math question, which is converted into text using speech recognition.

---

# Technology Stack

Python
Streamlit
Large Language Models (LLMs)
OCR (Optical Character Recognition)
Speech-to-Text Processing
Retrieval-Augmented Generation (RAG)

---

# Project Structure

```
Multimodal-Math-Mentor
│
├── agents
│   ├── parser_agent.py
│   ├── router_agent.py
│   ├── solver_agent.py
│   ├── verifier_agent.py
│   └── explainer_agent.py
│
├── tools
│   ├── ocr.py
│   ├── speech_to_text.py
│   └── rag
│       └── retriever.py
│
├── memory
│   └── memory_manager.py
│
├── utils
│   └── llm.py
│
├── app.py
├── requirements.txt
└── README.md
```

---

# How the System Works

1. User submits a math problem via text, image, or audio
2. Parser Agent interprets the problem
3. Router Agent identifies the mathematical domain
4. Retriever Agent gathers relevant context
5. Solver Agent computes the solution
6. Verifier Agent validates correctness
7. Explainer Agent generates step-by-step reasoning
8. Memory Manager stores the interaction

---

# Trade-offs and Design Considerations

While the system provides flexibility and transparency, several trade-offs exist:

Multi-agent systems may introduce **slightly higher latency** compared to single-model solutions.

OCR accuracy can depend on **image quality and handwriting clarity**.

Speech recognition may introduce **transcription errors** in noisy environments.

Retrieval-based reasoning depends on the **quality of indexed knowledge sources**.

These design decisions balance **accuracy, interpretability, and usability**.

---

# Key Achievements

Designed a **multi-agent reasoning architecture** for mathematical problem solving.

Implemented a **multimodal input pipeline** supporting text, image, and audio.

Integrated **OCR and speech-to-text technologies**.

Developed **Retrieval-Augmented Generation** for contextual reasoning.

Added a **solution verification stage** to improve reliability.

Built a **fully functional interactive web application using Streamlit**.

Successfully **deployed the application for real-time usage**.

---

# Future Improvements

Improve OCR accuracy for handwritten equations.

Add graph visualization for functions and equations.

Extend support for advanced symbolic mathematics.

Improve reasoning performance for complex multi-step problems.

Expand knowledge retrieval sources.

---

# Author

Karthik

---

# License

This project is open-source and available under the MIT License.

