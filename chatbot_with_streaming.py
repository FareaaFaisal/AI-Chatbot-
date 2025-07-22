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
    
    history = cl.user_session.get("chat history") or []
    history.append({"role": "user", "content": message.content})      # Append the new user messages to the history

    msg = cl.Message(content="")
    await msg.send()

    # Retrieving the Agent and Config from the user session
    agent:Agent = cast(Agent, cl.user_session.get("agent"))
    config:RunConfig = cast(RunConfig, cl.user_session.get("config"))
 

    try:
        print("\n[CALLING_AGENT_WITH_CONTEXT]\n", history, "\n")

        # Run the agent with the provided history and config
        result = Runner.run_streamed(agent, history, run_config=config)
        async for event in result.stream_events():  # token ka chota part bante hi ui me stream hota rahe ga
            if event.type == "raw_response_event" and hasattr(event.data, 'delta'): # check if the response from ai is live and saves all new lines to tokens
                token = event.data.delta
                await msg.stream_token(token)  # Stream the token to the UI one by one as it is generated
            
        await msg.update()  # This line is crucial to end the spinner/loading after the response is fully streamed
        
        history.append({"role": "assistant", "content": msg.content})  # Append the final output to the history
        cl.user_session.set("chat history", history)  # Update the chat history in the user session

        print(f"User: {message.content}")
        print(f"Assistant: {msg.content}")

    except Exception as e:
        await msg.update(content = f"Error: {str(e)}")  # Update the message in the chat with the error message
        print(f"Error: {str(e)}")