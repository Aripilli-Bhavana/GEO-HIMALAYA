import re
from langchain_community.llms import Ollama
from langchain.chains import LLMChain
from helper import prompt_helper

MODEL_NAME = "mistral"

def extract_query_tag(response: str) -> str:
    """
    Extracts the SQL query enclosed within the <Query> tags.
    """
    match = re.search(r"<Query:\s*(.*?)\s*>", response, re.DOTALL)
    return match.group(1) if match else "No <Query> tag found in the response."

def generate_responses(user_query: str, num_responses: int = 2):
    llm = Ollama(model=MODEL_NAME)
    query_chain = LLMChain(llm=llm, prompt=prompt_helper.get_prompt_template())
    response = query_chain.run(user_query=user_query, metadata=prompt_helper.get_metadata())
    sql_query = extract_query_tag(response)
    return sql_query

