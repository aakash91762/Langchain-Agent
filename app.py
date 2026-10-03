import os
import requests
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_react_agent, AgentExecutor
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain import hub
from langchain.tools import tool
from langchain_core.prompts import PromptTemplate

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Agent Playground",
    page_icon="🤖",
    layout="wide"
)


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
WEATHERSTACK_API_KEY = os.getenv("WEATHERSTACK_API_KEY")


# =========================================================
# CHECK API KEYS
# =========================================================

if not GOOGLE_API_KEY:
    st.error("GOOGLE_API_KEY is missing from .env")
    st.stop()

if not TAVILY_API_KEY:
    st.error("TAVILY_API_KEY is missing from .env")
    st.stop()

if not WEATHERSTACK_API_KEY:
    st.error("WEATHERSTACK_API_KEY is missing from .env")
    st.stop()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("⚙️ Agent Configuration")

    st.divider()

    st.subheader("🧠 Model")

    st.write("Gemini 3 Flash Preview")
    st.caption("Temperature: 0.3")

    st.divider()

    st.subheader("🛠️ Tools")

    st.info(
        "🔎 Tavily Search\n\n"
        "Search the web for current information."
    )

    st.info(
        "🌤️ WeatherStack\n\n"
        "Get current weather information."
    )

    st.divider()

    st.subheader("🧩 Agent")

    st.write("ReAct Agent")
    st.caption("LangChain AgentExecutor")

    st.divider()

    st.subheader("💡 Example Queries")

    st.write(
        "• Find the capital of India and its current weather."
    )

    st.write(
        "• Find the current weather in Mumbai."
    )

    st.write(
        "• What is the latest news about AI?"
    )

    st.write(
        "• Who is the current CEO of OpenAI?"
    )

    st.divider()

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()


# =========================================================
# MAIN HEADER
# =========================================================

st.title("🤖 Agent Playground")

st.caption(
    "LangChain agent testing console"
)

st.divider()


# =========================================================
# INTRO
# =========================================================

st.info(
    """
    **LangChain Agent Playground**

    Test your Gemini-powered ReAct agent with:

    🔎 Web Search  
    🌤️ Current Weather
    """
)


# =========================================================
# TAVILY SEARCH TOOL
# =========================================================

search_tool = TavilySearchResults(
    max_results=2
)


# =========================================================
# GEMINI MODEL
# =========================================================

# llm = ChatGoogleGenerativeAI(
#     model="gemini-3-flash-preview",
#     temperature=0.3,
#     google_api_key=GOOGLE_API_KEY
# )
llm = ChatGroq(
    model="qwen/qwen3.8-27b",
    temperature=0.3,
    groq_api_key=GROQ_API_KEY
)


# =========================================================
# WEATHER TOOL
# =========================================================

@tool
def get_weather_data(city: str) -> str:
    """
    Fetch current weather information for a city.
    """

    try:

        url = (
            "https://api.weatherstack.com/current"
            f"?access_key={WEATHERSTACK_API_KEY}"
            f"&query={city}"
        )

        response = requests.get(
            url,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        if "current" not in data:

            return (
                f"Could not fetch weather data for {city}."
            )

        current = data["current"]

        temperature = current.get(
            "temperature",
            "N/A"
        )

        description = current.get(
            "weather_descriptions",
            ["N/A"]
        )[0]

        humidity = current.get(
            "humidity",
            "N/A"
        )

        wind_speed = current.get(
            "wind_speed",
            "N/A"
        )

        return (
            f"City: {city}\n"
            f"Temperature: {temperature}°C\n"
            f"Weather: {description}\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind_speed} km/h"
        )

    except Exception as e:

        return (
            f"Weather API error: {str(e)}"
        )


# =========================================================
# TOOLS
# =========================================================

tools = [
    search_tool,
    get_weather_data
]


# =========================================================
# REACT PROMPT
# =========================================================

# prompt = hub.pull(
#     "hwchase17/react",
#     dangerously_pull_public_prompt=True
# )
prompt = PromptTemplate.from_template(
    """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}"""
)


# =========================================================
# CREATE AGENT
# =========================================================

agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)


# =========================================================
# AGENT EXECUTOR
# =========================================================

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=5
)


# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# =========================================================
# CONVERSATION
# =========================================================

st.subheader("💬 Agent Conversation")

st.caption(
    "Ask a question and the agent will decide which tool to use."
)


# =========================================================
# SHOW PREVIOUS MESSAGES
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# =========================================================
# CHAT INPUT
# =========================================================

user_input = st.chat_input(
    "Ask your AI agent something..."
)


# =========================================================
# RUN AGENT
# =========================================================

if user_input:

    # -----------------------------------------------------
    # USER MESSAGE
    # -----------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):

        st.markdown(user_input)


    # -----------------------------------------------------
    # AGENT RESPONSE
    # -----------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "🤔 Agent is thinking..."
        ):

            try:

                response = agent_executor.invoke(
                    {
                        "input": user_input
                    }
                )

                answer = response.get(
                    "output",
                    "No response generated."
                )

                st.markdown(answer)

                # Save response
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception as e:

                error_text = str(e)

                if "429" in error_text or "ResourceExhausted" in error_text:

                    st.warning(
                        """
                        ⚠️ **Gemini API quota exceeded**

                        Your Gemini API free-tier request quota has been
                        exhausted.

                        Please wait for the quota to reset or check your
                        Gemini API billing/quota settings.
                        """
                    )

                else:

                    st.error(
                        f"❌ Agent error:\n\n{error_text}"
                    )