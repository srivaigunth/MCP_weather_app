import asyncio
from langchain_groq import ChatGroq

from dotenv import load_dotenv
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from mcp_use import MCPAgent, MCPClient
import os

async def run_memory_chat():
    """Run a chat usig MCPAgent """
    #load env variables
    load_dotenv()
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY", "default_value_here")

    #config file path
    config_file = "server/weather.json"

    print("STARTING CHAT....")

    #Create an MCP client with Agent memory
    client = MCPClient.from_config_file(config_file)
    llm = ChatGroq(model = "qwen-qwq-32b")

    #Creating an agent with MEMORY
    agent = MCPAgent(
        llm = llm,
        client = client,
        max_steps = 10,
        memory_enabled = True,
    )

    print("\n Welcome to the CLI chatbot")
    print("type 'clear' to clear conversation history")
    print("type 'exit' to get the hell out")
    print("--------------------------------")

    try:
        while(True):
            user_input = input("You : ").strip()
            if(user_input == 'exit'):
                print("BYEEEEEEEEEE....")
                break
            if(user_input == 'clear'):
                agent.clear_conversation_history()
                continue
            
            print("\n Assistant : ", end = "", flush = True)

            try:
                response = await agent.run(user_input)
                print(response)
            except Exception as e:
                print("error", e) 
    finally:
        #Clean up
        if client and client.sessions:
            await client.close_all_sessions()

if __name__ == "__main__":
    asyncio.run(run_memory_chat())