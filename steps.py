from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool
import classes as cls
import pdb

def write_query(state: cls.State):
    prompt = state["prompt_template"].invoke(
        {
            "dialect": state["database"].dialect,
            "top_k": 50000,
            "table_info": state["database"].get_table_info(),
            "question": state["question"],
        }
    )
    structured_llm = state["llm"].with_structured_output(cls.QueryOutput)
    result = structured_llm.invoke(prompt)
    state["query"] = result["query"]
    return state

def execute_query(state: cls.State):
    execute_query_tool = QuerySQLDatabaseTool(db=state["database"])
    state["result"] = execute_query_tool.invoke(state["query"])
    # print(f"\nResult: {state["result"]}\n")
    return state

def predict(state: cls.State):
    pass

def generate_answer(state: cls.State):
    prompt = (
        "Given the following user question, corresponding SQL query, "
        "and SQL result, answer the user question.\n\n"
        f"Question: {state['question']}\n"
        f"SQL Query: {state['query']}\n"
        f"SQL Result: {state['result']}"
    )
    response = state["llm"].invoke(prompt)
    state["answer"] = response.content
    return state