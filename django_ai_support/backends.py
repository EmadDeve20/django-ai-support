from langchain_core.messages import HumanMessage

from .graphs import init_agent

def normal_chat_with_ai(user_message:str, thread_id:str) -> str:
    """
    function to chat with AI

    Args:
        user_message (str): message of user
        thread_id (str): id of thread to save messages

    Returns:
        str: return coming message
    """

    agent = init_agent()

    config = {"configurable": {"thread_id": str(thread_id)}}

    messages = [
        HumanMessage(user_message)
    ]

    ai_response = agent.invoke({"messages": messages}, config=config)

    ai_response = ai_response["messages"][-1].content

    return ai_response

