from langchain.agents import initialize_agent, Tool
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
from langchain.tools.python.tool import PythonREPLTool
from validators.dag_valid import validate_dag
from utils.git_watch import check_for_new_dags
import subprocess
import os
from dotenv import load_dotenv






load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")


# Define tool for DAG validation
def dag_validation_tool():
    new_dags = check_for_new_dags("dags/")
    results = []
    for dag in new_dags:
        result = validate_dag(os.path.join("dags", dag))
        results.append({"dag": dag, "result": result})
    return results

# Define tool for DAG deployment
def deploy_dags():
    try:
        subprocess.run(["airflow", "dags", "list"], check=True)
        return "DAGs deployed successfully."
    except subprocess.CalledProcessError as e:
        return f"Deployment failed: {e}"

# Define LangChain tools
custom_tools = [
    Tool(
        name="ValidateDAGs",
        func=lambda x: dag_validation_tool(),
        description="Validates newly added DAGs in the dags/ directory"
    ),
    Tool(
        name="DeployDAGs",
        func=lambda x: deploy_dags(),
        description="Deploys the DAGs using Airflow command line"
    ),
    PythonREPLTool()
]

# Initialize the AI agent
llm = ChatOpenAI(temperature=0, model_name="gpt-4")
agent = initialize_agent(
    custom_tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

def run_orchestration():
    print("Starting AI Orchestrator...")
    result = agent.run("Check for new DAGs, validate them, and deploy if valid.")
    print("Result:", result)

if __name__ == "__main__":
    run_orchestration()
