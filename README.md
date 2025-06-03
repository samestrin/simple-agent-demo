# Simple Agent Demo

[![Star on GitHub](https://img.shields.io/github/stars/samestrin/simple-agent-demo?style=social)](https://github.com/samestrin/simple-agent-demo/stargazers) [![Fork on GitHub](https://img.shields.io/github/forks/samestrin/simple-agent-demo?style=social)](https://github.com/samestrin/simple-agent-demo/network/members) [![Watch on GitHub](https://img.shields.io/github/watchers/samestrin/simple-agent-demo?style=social)](https://github.com/samestrin/simple-agent-demo/watchers)

![Version 1.0.0](https://img.shields.io/badge/Version-1.0.0-blue) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg) ](https://opensource.org/licenses/MIT)[![Built with Python](https://img.shields.io/badge/Built%20with-Python-green)](https://www.python.org/)


A simple AI agent demo built with LangChain and OpenAI. This project defines and integrates multiple tools, Wikipedia search tool and a safe calculator tool, and shows how the agent reasons about each incoming question to choose the correct tool before returning an answer.

## Project Structure

```text
.
├── .env
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── simple_agent/
    ├── agent_demo.py
    └── tools.py
```

## Features

-   **Wikipedia Search**: The agent can use Wikipedia to answer general knowledge questions.
-   **Safe Calculator**: The agent includes a calculator tool that safely evaluates mathematical expressions without using `eval()`.
-   **Error Handling**: Robust error handling for API calls and tool usage.
-   **Type Hinting & Docstrings**: Code is annotated with type hints and includes comprehensive docstrings for better readability and maintainability.

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/samestrin/simple-agent-demo
cd simple-agent-demo
```

### 2. Create a Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Install the required packages using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

**Dependencies Overview:**

*   `langchain`: The core framework for building applications with LLMs.
*   `openai`: Python client library for the OpenAI API.
*   `wikipedia`: A Python library that makes it easy to access and parse data from Wikipedia.

### 4. Set Up Environment Variables

Create a `.env` file in the project root by copying the `.env.example` file:

```bash
cp .env.example .env
```

Open the `.env` file and add your OpenAI API key:

```text
OPENAI_API_KEY="sk-your_openai_api_key_here"
```

Alternatively, you can set the `OPENAI_API_KEY` as an environment variable in your shell:

```bash
export OPENAI_API_KEY="sk-your_openai_api_key_here"
```

LangChain will automatically pick up the API key from either the `.env` file or the shell environment.

## Running the Demo

To run the agent demo, execute the `simple_agent` script from the project root directory:

```bash
python -m simple_agent.agent_demo
```

The demo will run through a series of example questions that demonstrate the agent's capabilities:

1.  A factual question (e.g., "Who was Ada Lovelace and why is she important?") - uses the `WikipediaTool`.
2.  A mathematical calculation (e.g., "What is 17 * (24 - 5)?") - uses the `CalculatorTool`.
3.  Another general knowledge question (e.g., "Tell me something about Art Deco jewelry.") - uses the `WikipediaTool`.

## How It Works

The agent, implemented in `simple_agent/agent_demo.py`, uses a "zero-shot-react-description" agent type from LangChain. This means it:

1.  Analyzes the input question to determine the most appropriate tool to use.
2.  Calls the selected tool with the necessary input (e.g., the search query for Wikipedia or the expression for the calculator).
3.  Processes the tool's output to formulate a final answer to the user's question.

The agent has access to two primary tools defined in `simple_agent/tools.py`:

*   **WikipediaTool**: Searches Wikipedia for a given query and returns a concise summary from the relevant article.
*   **CalculatorTool**: Safely evaluates mathematical expressions using Python's `ast` module to parse the expression and `operator` module for calculations, avoiding the security risks of `eval()`.

## Code Overview

### `simple_agent/agent_demo.py`

*   Initializes the OpenAI LLM.
*   Sets up the `WikipediaTool` and `CalculatorTool`.
*   Creates the LangChain agent.
*   Includes a main function that runs example questions and handles potential OpenAI API errors (e.g., `AuthenticationError`, `RateLimitError`).

### `simple_agent/tools.py`

*   **WikipediaTool**: Inherits from `BaseTool`. Its `_run` method takes a search query, uses the `wikipedia` library to fetch and summarize the article, and returns the summary.
*   **CalculatorTool**: Inherits from `BaseTool`. Its `_run` method takes a mathematical expression string.
    *   It first validates the expression using a regular expression to allow only numbers, basic arithmetic operators, parentheses, and spaces.
    *   It then parses the expression into an Abstract Syntax Tree (AST) using `ast.parse()`.
    *   A nested function, `eval_expr`, recursively traverses the AST, performing calculations using the `operator` module for whitelisted operations (addition, subtraction, multiplication, division, unary minus).
    *   This approach ensures that only valid, safe mathematical operations are executed.

## Extending the Agent

You can extend this agent by:

1.  Adding new custom tool classes (inheriting from `BaseTool`) in `simple_agent/tools.py` or a new tools file.
2.  Instantiating and registering these new tools within the `tools` list in `simple_agent/agent_demo.py`.
3.  Testing the agent with new types of questions that would require the new tools.

## Safety Notes

The `CalculatorTool` has been designed with safety in mind. By using `ast.parse` and a whitelisting approach for operations, it avoids the significant security vulnerabilities associated with using `eval()` on arbitrary string inputs.

## License

This project is available under the MIT License. See the [LICENSE](LICENSE) file for details.

## Share

[![Twitter](https://img.shields.io/badge/X-Tweet-blue)](https://twitter.com/intent/tweet?text=Check%20out%20this%20awesome%20project!&url=https://github.com/samestrin/simple-agent-demo) [![Facebook](https://img.shields.io/badge/Facebook-Share-blue)](https://www.facebook.com/sharer/sharer.php?u=https://github.com/samestrin/simple-agent-demo) [![LinkedIn](https://img.shields.io/badge/LinkedIn-Share-blue)](https://www.linkedin.com/sharing/share-offsite/?url=https://github.com/samestrin/simple-agent-demo)