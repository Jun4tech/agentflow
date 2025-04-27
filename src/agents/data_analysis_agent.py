from langchain_ollama import ChatOllama
from dotenv import load_dotenv
from src.tools.sql_db import describe_tables_schema, execute_sql_query
from langgraph.graph import StateGraph, START, END
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain_core.prompts import ChatPromptTemplate
from langgraph.checkpoint.memory import MemorySaver
from src.agents.utils import extract_deepseek_response_from_tag

load_dotenv()
memory = MemorySaver()


class State(TypedDict):
    tablename_result: str
    tables_schema: str
    sql_query: str
    sql_result: str
    messages: Annotated[list, add_messages]


class DataAnalystLLM:
    def __init__(self, model: str):
        self.model = model
        self.llm = ChatOllama(model=model, temperature=0)

    def chatbot(self, state: State):
        return {"messages": [self.llm.invoke(state["messages"])]}


def identify_table_from_input(state: State):
    """
    Identify the interested table related to user input
    """

    sys_prompt = """
        Given table name, along with the description of the table below:
        sys_expense_master: Contains the master data of all expenses
        sys_expense_detail: Contains the detail data of all expenses
        Please identifies tables which the query might be related to.
        Please return the result of identified tables wrapped in <table> tags.
        For example:<table>sys_expense_master,syn_expense_detail</table>
    """

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", sys_prompt),
            ("user", "{messages}"),
        ]
    ).format_prompt(messages=state["messages"])

    resoning_llm = ChatOllama(model="deepseek-r1:14B", temperature=0)
    response = resoning_llm.invoke(prompt)
    result = extract_deepseek_response_from_tag(str(response.content), tag="table")
    return {"tablename_result": result}


def get_tables_schema(state: State):
    """
    Get the schema of identified tables
    """

    result = describe_tables_schema(state["tablename_result"])
    result_str = ""
    for item in result:
        result_str += f"{item['COLUMN_NAME']} : {item['DATA_TYPE']}, "

    return {"tables_schema": result_str}


def generate_sql_based_on_schema(state: State):
    """
    Generate SQL query based on the schema
    """
    sys_prompt = f"""
        Do not give any explanation, only give the SQL query.
        Please generate the SQL query to help answer the question of "{state["messages"][0].text()}"
        with given schema of the tables ({state["tablename_result"]}):
        {state["tables_schema"]}
        TotalExpenses : Total amount of expenses
        Please make sure the generated SQL Query wrapped around <sql> and </sql> tags.
        For example:<sql>SELECT * FROM your_table</sql>
    """

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", sys_prompt),
            ("user", "{messages}"),
        ]
    ).format_prompt(messages=state["messages"])

    resoning_llm = ChatOllama(model="deepseek-r1:14B", temperature=0)
    response = resoning_llm.invoke(prompt)
    result = extract_deepseek_response_from_tag(str(response.content), tag="sql")
    return {"sql_query": result}


def get_sql_query_result(state: State):
    """
    Execute the SQL query and return the result
    """

    print(f"SQL Query: {state['sql_query']}")
    results = execute_sql_query(state["sql_query"])
    # convert the result to string
    result_str = ""
    for item in results:
        for key, value in item.items():
            result_str += f"{key} : {value}, "
        result_str += "\n"
    # if the result is empty, return empty string
    if not result_str:
        result_str = "No result found"
    print(result_str)
    return {"sql_result": result_str}


def summarize_result(state: State):
    """
    Summarize the result of SQL query
    """

    sys_prompt = f"""
        Please answer the question of "{state["messages"][0].text()}"
        based on the data below:
        {state["sql_result"]}
        Please give an answer in a concise and clear manner.
    """

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", sys_prompt),
            ("user", "{messages}"),
        ]
    ).format_prompt(messages=state["messages"])

    resoning_llm = ChatOllama(model="deepseek-r1:14B", temperature=0)
    response = resoning_llm.invoke(prompt)
    response.content = extract_deepseek_response_from_tag(
        response=str(response.content)
    )
    return {"messages": [response]}


graph_builder = StateGraph(State)
graph_builder.add_node("identify_table_from_input", identify_table_from_input)
graph_builder.add_node("get_tables_schema", get_tables_schema)
graph_builder.add_node("generate_sql_based_on_schema", generate_sql_based_on_schema)
graph_builder.add_node("get_sql_query_result", get_sql_query_result)
graph_builder.add_node("summarize_result", summarize_result)

graph_builder.add_edge(START, "identify_table_from_input")
graph_builder.add_edge("identify_table_from_input", "get_tables_schema")
graph_builder.add_edge("get_tables_schema", "generate_sql_based_on_schema")
graph_builder.add_edge("generate_sql_based_on_schema", "get_sql_query_result")
graph_builder.add_edge("get_sql_query_result", "summarize_result")
graph_builder.add_edge("summarize_result", END)
data_analysis_graph = graph_builder.compile(checkpointer=memory)
