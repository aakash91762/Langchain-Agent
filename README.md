Installation
# 1. Create the environment named 'langagent'
python3 -m venv langagentNew

# 2. Activate it
source langagentNew/bin/activate
pip install -r requirements.txt
pip install python-dotenv langchain-google-genai langchain-community tavily-python langchain requests