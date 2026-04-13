import os
from dotenv import load_dotenv

from vanna import Agent, AgentConfig
from vanna.core.registry import ToolRegistry
from vanna.core.user import UserResolver, User, RequestContext

from vanna.tools import RunSqlTool, VisualizeDataTool
from vanna.tools.agent_memory import (
    SaveQuestionToolArgsTool,
    SearchSavedCorrectToolUsesTool
)

from vanna.integrations.sqlite import SqliteRunner
from vanna.integrations.local.agent_memory import DemoAgentMemory
#from vanna.integrations.google import GeminiLlmService
from vanna.integrations.openai import OpenAILlmService 
from vanna.servers.fastapi import VannaFastAPIServer
from sql_validator import validate_sql
load_dotenv()



def create_llm(api_key):
    
    try :
        llm = OpenAILlmService(
        api_key=os.getenv("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1",
        model="openai/gpt-oss-120b"  
        )
    except Exception as e:
        print(f"Error initializing LLM: {e}")
        raise e
    return llm



'''
def create_llm(api_key):
    return GeminiLlmService(api_key=api_key, model="gemini-2.0-flash", temperature=0.2)'''


def create_sqlite_runner(database_path=r"D:\SQL_LLM\clinic.db"):
    return SqliteRunner(database_path=database_path)


def create_memory():
    return DemoAgentMemory()


def create_tool_registry(runner, memory):
    tools = [
        RunSqlTool(runner),
        VisualizeDataTool(),


        SaveQuestionToolArgsTool(),
        SearchSavedCorrectToolUsesTool()
    ]

    return ToolRegistry(tools)


class SimpleUserResolver(UserResolver):
    async def resolve_user(self, request_context: RequestContext) -> User:
        return User(
            id="default_user",
            email="default@example.com",
            group_memberships=["admin"]
        )


def create_user_context():
    user = User(id="default_user")

    resolver = SimpleUserResolver()

    context = RequestContext(user=user)

    return resolver, context




class SafeRunSqlTool(RunSqlTool):
    def run(self, query: str, context=None):
        

        is_valid, message = validate_sql(query)

        if not is_valid:
            return {
                "error": f"SQL Validation Failed: {message}"
            }

        try:
            result = super().run(query, context)

            if not result:
                return {
                    "message": "No data found."
                }

            return result

        except Exception as e:
            return {
                "error": f"Database execution failed: {str(e)}"
            }

def create_agent(llm, registry, memory, resolver):
    return Agent(
        llm_service=llm,
        tool_registry=registry,
        user_resolver=resolver,
        agent_memory=memory
    )


def setup_vanna():
    api_key = load_environment()

    llm = create_llm(api_key)
    memory = create_memory()

    runner = SqliteRunner(database_path="clinic.db")

    db_tool = SafeRunSqlTool(sql_runner=runner)

    tools = ToolRegistry()
    tools.register_local_tool(db_tool, access_groups=['admin', 'user'])
    tools.register_local_tool(VisualizeDataTool(), access_groups=['admin', 'user'])
    tools.register_local_tool(SaveQuestionToolArgsTool(), access_groups=['admin'])
    tools.register_local_tool(SearchSavedCorrectToolUsesTool(), access_groups=['admin', 'user'])

    resolver = SimpleUserResolver()

    agent = Agent(
        llm_service=llm,
        tool_registry=tools,
        user_resolver=resolver,
        agent_memory=memory
    )
    agent.system_message = """

        You are a SQLite expert for a clinic database with these tables:
        - patients(id, first_name, last_name, email, phone, date_of_birth, gender, city, registered_date)
        - doctors(id, name, specialization, department, phone)
        - appointments(id, patient_id, doctor_id, appointment_date, status, notes)
        - treatments(id, appointment_id, treatment_name, cost, duration_minutes)
        - invoices(id, patient_id, invoice_date, total_amount, paid_amount, status)

        IMPORTANT:
        - Always return final answer in this format:
        - must use bulltet points and markdown formatting for clarity

        ANSWER FORMAT:
        SQL: <query>
        Explanation: <short explanation>
        Answer: <final number or result>

        - SQL & Answer must ALWAYS be present
        - NEVER return only tool output
        """
    print("Vanna 2.x agent initialized successfully!")

    return agent, None



'''def test_agent():
    agent, context = setup_vanna()

    question = "How many patients are there?"

    response = agent.run(
        input=question,
        context=context
    )

    print("\n🧠 Question:", question)
    print("📊 Response:", response)'''




def test_agent():
    agent, _ = setup_vanna()

    server = VannaFastAPIServer(agent)
    server.run()



if __name__ == "__main__":
    test_agent()