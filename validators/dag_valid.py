from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

def validate_dag(dag_code: str) -> bool:
    prompt = ChatPromptTemplate.from_template(
        """You are a DAG validation expert. Given this Airflow DAG code, check if:
        1. It's syntactically correct.
        2. It defines a DAG object.
        3. It uses proper operators.
        
        Return only 'Valid' or 'Invalid' with a short reason.

        DAG code:
        ```python
        {dag_code}
        ```"""
    )
    
    llm = ChatOpenAI(temperature=0, model="gpt-4")
    chain = prompt | llm
    response = chain.invoke({"dag_code": dag_code})
    return "Valid" in response.content
