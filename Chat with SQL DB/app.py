import streamlit as st
from pathlib import Path
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq

st.set_page_config(page_title="Chat with SQL DB", layout="wide", page_icon=":bar_chart:")
st.title("Chat with SQL DB")

LOCALDB = "USE_LOCAL_DB"
MYSQL = "USE_MYSQL"

radio_opt = ["Use Local DB", "Use MySQL"]

selected_opt = st.sidebar.radio("Select Database", radio_opt)

if radio_opt.index(selected_opt)==1:
    db_type = MYSQL
    mysql_host = st.sidebar.text_input("MySQL Host", "localhost")
    mysql_user = st.sidebar.text_input("MySQL User", "root")
    mysql_password = st.sidebar.text_input("MySQL Password", type="password")
    mysql_db = st.sidebar.text_input("MySQL DB")
else:
    db_type = LOCALDB

api_key = st.sidebar.text_input("Groq API Key",type="password")

if not db_type:
    st.info("Please enter the database information")

if not api_key:
    st.info("Please enter the Groq API Key")

## LLM Model
llm = ChatGroq(groq_api_key=api_key, model_name="Llama3-8b-8192",streaming=True)

@st.cache_resource(ttl="2h")
def configure_db(db_type, mysql_host=None, mysql_user=None, mysql_password=None, mysql_db=None):
    if db_type == LOCALDB:
        dbfilepath= (Path(__file__).parent / "student.db").absolute()
        creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
        return SQLDatabase(create_engine("sqlite://", creator=creator))
    elif db_type == MYSQL:
        if not (mysql_host and mysql_user and mysql_password and mysql_db):
            st.error("Please enter the MySQL database information")
            st.stop()
        return SQLDatabase(create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"))
if db_type == MYSQL:
    db = configure_db(db_type, mysql_host, mysql_user, mysql_password, mysql_db)
else:
    db = configure_db(db_type)

## toolkit
toolkit = SQLDatabaseToolkit(db)

## agent
agent = create_sql_agent(
    llm = llm,
    toolkit = toolkit,
    verbose = True,
    agent_type= AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
    st.session_state["messages"] = [{
        "role": "assistant",
        "content": "How can I help you?"
    }]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_query = st.chat_input(placeholder="Ask anything from the database")

if user_query:
    st.session_state.messages.append({
        "role": "user",
        "content": user_query
    })
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        streamlit_callback_handler = StreamlitCallbackHandler(st.container)
        response = agent.run(user_query, callbacks=[streamlit_callback_handler])
        st.session_state.messages.append({
            "role": "system",
            "content": response
        })
        st.write(response)