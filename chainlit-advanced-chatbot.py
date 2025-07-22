import os                         # to connect .env with this code
from dotenv import load_dotenv    # this loads environment variables from a .env file like our API key
from typing import cast           # to cast types for better type checking
import chainlit as cl
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents .run import RunConfig # Configuration object for contolling ai agents

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key exists
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

@cl.on_chat_start
async def main():

    #Reference: https://ai.google.dev/gemini-api/docs/openai
    external_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )

    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client
    )

    config = RunConfig(
        model=model,
        model_provider=external_client,
        tracing_disabled=True
    )

    # Creating an empty list to store user chats
    cl.user_session.set("chat history", [])
    cl.user_session.set("config", config)

    # Create the agent
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant. Answer the user's questions to the best of your ability.",
        model=model,
    )

    # Storing the agent in the user session
    cl.user_session.set("agent", agent)
    await cl.Message(content = "Welcome to the Fareaa's AI Assistant! How can I help you today?").send()  

@cl.on_message
async def main(message: cl.Message):     # When a message is received and reply is generating so a waiting message is sent
    msg = cl.Message(content="Thinking...")
    await msg.send()

    # Retrieving the Agent and Config from the user session
    agent:Agent = cast(Agent, cl.user_session.get("agent"))
    config:RunConfig = cast(RunConfig, cl.user_session.get("config"))
    history = cl.user_session.get("chat history") or []
    history.append({"role": "user", "content": message.content})      # Append the new user messages to the history

    try:
        print("\n[CALLING_AGENT_WITH_CONTEXT]\n", history, "\n")

        # Run the agent with the provided history and config
        result = Runner.run_sync(
            starting_agent= agent,
            input = history,
            run_config=config
        )

        response_content = result.final_output
        msg.content = response_content # Update the message content from "Thinking" to the actual agent's response
        await msg.update()             # Update the message in the chat with the response

        # Making new history to store user + agent conversations
        cl.user_session.set("chat history", result.to_input_list())

        print(f"User: {message.content}")
        print(f"Assistant: {response_content}")

    except Exception as e:
        msg.content = f"An error occurred: {str(e)}"
        await msg.update()
        print(f"Error: {str(e)}")