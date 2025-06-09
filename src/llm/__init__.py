import re
from langchain_community.llms import Ollama
from langchain.chains import LLMChain
from helper import prompt_helper, logger
from langchain.cache import InMemoryCache
from langchain.globals import set_llm_cache

MODEL_NAME = "mistral"
set_llm_cache(InMemoryCache())

def extract_query_tag(response: str) -> str:
    """
    Extracts the SQL query enclosed within the <Query> tags.
    """
    match = re.search(r"<Query:\s*(.*?)\s*>", response, re.DOTALL)
    return match.group(1) if match else "No <Query> tag found in the response."

def generate_responses(user_query: str):
    llm = Ollama(model=MODEL_NAME, temperature=0,top_p=0, top_k=1)
    query_chain = LLMChain(llm=llm, prompt=prompt_helper.get_prompt_template())
    response = query_chain.run({"user_query": user_query, "metadata": prompt_helper.get_metadata()})
    logger.log("INFO", f"LLM Resposne : {response}")
    return response

