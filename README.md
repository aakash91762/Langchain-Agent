Installation
# 1. Create the environment named 'langagent'
python3 -m venv langagentNew

# 2. Activate it
source langagentNew/bin/activate
pip install -r requirements.txt
pip install python-dotenv langchain-google-genai langchain-community tavily-python langchain requests

# 3. Push to github
1. git add . 
2. git commit -m "test"
3. git remote set-url origin https://github.com/aakash91762/Langchain-Agent.git
4. git remote add origin https://github.com/aakash91762/Langchain-Agent.git 
5.  git branch -M main   
6. git push -u origin main 

# 3. How to run stramlit
streamlit run main.py
