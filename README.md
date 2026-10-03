# 🤖 LangChain ReAct Agent with Gemini, Tavily & WeatherStack

A tool-using AI agent built with **LangChain**, **Google Gemini**, **Tavily Search**, and **WeatherStack**.

The agent uses the **ReAct (Reasoning + Acting)** pattern to understand a user's request, decide which tool is required, execute the tool, and generate a final response.

The project also includes a **Streamlit interface** for interacting with the agent through a web UI.

---

## 🚀 Features

* 🤖 Google Gemini-powered AI agent
* 🧠 LangChain ReAct agent architecture
* 🔎 Real-time web search using Tavily
* 🌤️ Current weather information using WeatherStack
* 🛠️ Custom LangChain tools using `@tool`
* 🔐 API keys managed using environment variables
* 🖥️ Streamlit web interface
* 🔄 Agent automatically selects the appropriate tool based on the user query

---

## 🏗️ Architecture

The application follows this flow:

```text
                         User Query
                             │
                             ▼
                  ┌─────────────────────┐
                  │   LangChain Agent   │
                  │     ReAct Agent     │
                  └──────────┬──────────┘
                             │
                             ▼
                    Google Gemini LLM
                             │
                             ▼
                  Decide which tool to use
                             │
                    ┌────────┴────────┐
                    │                 │
                    ▼                 ▼
             Tavily Search      WeatherStack
              Web Search         Weather API
                    │                 │
                    └────────┬────────┘
                             │
                             ▼
                       Tool Results
                             │
                             ▼
                       Final Answer
```

---

## 🧠 What is ReAct?

**ReAct** stands for **Reasoning + Acting**.

Instead of simply asking an LLM to generate an answer, the agent can decide when it needs to use an external tool.

For example:

```text
User:
Find the capital of India and then find its current weather.
```

The agent can determine:

```text
1. Identify the capital of India
        ↓
2. Identify that weather information is required
        ↓
3. Use WeatherStack
        ↓
4. Get the current weather
        ↓
5. Generate the final response
```

This allows the LLM to interact with external systems and retrieve information that may not be available in its training data.

---

# 🛠️ Technologies Used

| Technology    | Purpose                         |
| ------------- | ------------------------------- |
| Python        | Programming language            |
| LangChain     | Agent and tool framework        |
| Google Gemini | Large Language Model            |
| Tavily        | Real-time web search            |
| WeatherStack  | Current weather API             |
| Streamlit     | Web-based user interface        |
| python-dotenv | Environment variable management |
| Requests      | HTTP/API requests               |

---

# 📋 Prerequisites

Before starting, make sure you have:

* Python 3.9+
* Git
* Google Gemini API key
* Tavily API key
* WeatherStack API key

---

# 📦 Installation

## 1. Clone the repository

```bash
git clone https://github.com/aakash91762/Langchain-Agent.git
```

Navigate into the project:

```bash
cd Langchain-Agent
```

---

## 2. Create a Virtual Environment

Create a virtual environment named `langagentNew`:

```bash
python3 -m venv langagentNew
```

This creates an isolated Python environment for the project.

---

## 3. Activate the Virtual Environment

### macOS / Linux

```bash
source langagentNew/bin/activate
```

### Windows

```bash
langagentNew\Scripts\activate
```

After activation, you should see something similar to:

```text
(langagentNew)
```

in your terminal.

---

## 4. Install Dependencies


```bash
pip install python-dotenv langchain-google-genai langchain-community tavily-python langchain requests streamlit
```

---

# 🔑 API Configuration

The application requires API keys for Gemini, Tavily, and WeatherStack.

Create a file named:

```text
.env
```

in the root directory of the project.

Add the following:

```env
GOOGLE_API_KEY=your_google_api_key
TAVILY_API_KEY=your_tavily_api_key
WEATHERSTACK_API_KEY=your_weatherstack_api_key
```

The application loads these variables using:

```python
from dotenv import load_dotenv

load_dotenv()
```

and retrieves them using:

```python
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
WEATHERSTACK_API_KEY = os.getenv("WEATHERSTACK_API_KEY")
```

### ⚠️ Security

**Never commit your `.env` file to GitHub.**

Add the following to `.gitignore`:

```text
.env
__pycache__/
*.pyc
langagentNew/
```

---

# 🔎 Tavily Search Tool

Tavily provides the agent with real-time web search capabilities.

The search tool is initialized as:

```python
search_tool = TavilySearchResults(max_results=2)
```

For example:

```python
search_tool.invoke("Latest AI news")
```

The agent can decide to use Tavily when the user asks for information that requires web search.

### Example

```text
User:
What are the latest developments in AI?
```

The agent can use:

```text
Tavily Search
      ↓
Search the web
      ↓
Return relevant information
      ↓
Gemini generates the final response
```

---

# 🌤️ WeatherStack Tool

The project also contains a custom weather tool built using LangChain's `@tool` decorator.

```python
@tool
def get_weather_data(city: str) -> str:
    """
    Fetch current weather information for a city.
    """
```

The tool calls the WeatherStack API to retrieve current weather information.

Conceptually:

```text
Agent
  ↓
get_weather_data("Delhi")
  ↓
WeatherStack API
  ↓
Current weather
  ↓
Agent
  ↓
Final response
```

---

# 🔧 LangChain Tools

The tools are combined into a list:

```python
tools = [
    search_tool,
    get_weather_data
]
```

The agent can then choose between these tools depending on the user's request.

For example:

| User Request                                        | Tool                     |
| --------------------------------------------------- | ------------------------ |
| "What is the latest AI news?"                       | Tavily                   |
| "What is the weather in Delhi?"                     | WeatherStack             |
| "Find the capital of India"                         | LLM / Tavily if required |
| "Find the capital of India and its current weather" | WeatherStack + reasoning |

---

# 🤖 Creating the Agent

The ReAct agent is created using LangChain:

```python
agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)
```

The agent receives:

* An LLM
* A collection of tools
* A ReAct prompt

The LLM is configured using Google Gemini:

```python
llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    temperature=0.3,
)
```

---

# ⚙️ Agent Executor

The `AgentExecutor` is responsible for running the agent and its tools.

```python
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)
```

The executor manages the interaction between:

```text
User Input
    ↓
Agent
    ↓
Tool Selection
    ↓
Tool Execution
    ↓
Tool Result
    ↓
Agent
    ↓
Final Response
```

---

# ▶️ Running the Application

There are two ways to run the project.

## Option 1 — Run with Python

Run:

```bash
python main.py
```

The agent executes the configured query:

```python
response = agent_executor.invoke({
    "input": (
        "Find the capital of India "
        "and then find its current weather."
    )
})
```

The final response is printed using:

```python
print(response["output"])
```

---

# 🖥️ Running the Streamlit Application

To start the Streamlit interface:

```bash
streamlit run main.py
```

Streamlit will start a local web server.

You can then open the URL displayed in the terminal, typically:

```text
http://localhost:8501
```

The Streamlit interface allows you to interact with the AI agent through a web browser.

---

# 📁 Project Structure

The recommended project structure is:

```text
Langchain-Agent/
│
├── main.py
├── README.md
├── requirements.txt
├── .env
├── .gitignore
│
└── langagentNew/
```

### File Description

| File               | Description                        |
| ------------------ | ---------------------------------- |
| `main.py`          | Main application and agent logic   |
| `requirements.txt` | Python dependencies                |
| `.env`             | API keys and environment variables |
| `.gitignore`       | Files excluded from Git            |
| `README.md`        | Project documentation              |
| `langagentNew/`    | Python virtual environment         |

> `langagentNew/` should not be committed to GitHub.

---

# 📄 requirements.txt

The project dependencies can be stored in `requirements.txt`.

Example:

```text
langchain
langchain-google-genai
langchain-community
tavily-python
python-dotenv
requests
streamlit
```


---

# 🔐 Security Best Practices

Do not hardcode API keys in your Python code.

### ❌ Avoid

```python
GOOGLE_API_KEY = "your-secret-api-key"
```

### ✅ Recommended

```python
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
```

Store the actual key inside `.env`:

```env
GOOGLE_API_KEY=your_google_api_key
```

And make sure `.env` is included in `.gitignore`.




# 🧪 Example Queries

Once the Streamlit application is running, you can try queries such as:

### Weather

```text
What is the current weather in Delhi?
```

### Web Search

```text
What are the latest developments in generative AI?
```

### Multi-tool Query

```text
Find the capital of India and then find its current weather.
```

### Research

```text
Search the web and tell me about the latest AI agent frameworks.
```

---

# 🎯 Use Cases

This project demonstrates the foundation for building more advanced AI agents.

Potential applications include:

* 🌦️ Weather assistants
* 🔎 Research agents
* 📰 News assistants
* 📚 Knowledge assistants
* 🏢 Enterprise AI assistants
* 🛒 Product research agents
* 📊 Data/research agents
* 🤖 Multi-tool AI agents
* 💬 Customer support assistants

---

---

# 🧩 Learning Goals

This project is designed to demonstrate the following concepts:

* LangChain
* LLM integration
* Google Gemini
* ReAct agents
* Agent executors
* Tool calling
* Custom LangChain tools
* API integration
* Environment variables
* Tavily web search
* WeatherStack API
* Streamlit
* Git and GitHub

---

# 👨‍💻 Author

**Aakash Solanki**

Built as a hands-on project for learning and experimenting with:

**LangChain · AI Agents · Google Gemini · Tool Calling · Tavily · WeatherStack · Streamlit**

---

## ⭐ If you find this project useful

Feel free to fork the repository, experiment with additional tools, and extend the agent with your own use cases.
