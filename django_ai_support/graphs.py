import redis
import psycopg

from psycopg_pool import ConnectionPool
from pymongo import MongoClient

from langgraph.graph import START, END, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langgraph.checkpoint.memory import MemorySaver, InMemorySaver
from langgraph.checkpoint.redis import RedisSaver
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.checkpoint.mongodb import MongoDBSaver


from .settings import api_settings

if api_settings.SYSTEM_PROMPT:
    system_prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", api_settings.SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

else:
    system_prompt_template = None


def generate_short_term_memory() -> InMemorySaver | PostgresSaver | RedisSaver | MongoDBSaver:
    """
    generating short term memory
    
    :return: return one of MemorySaver object by Django Ai Support Settings
    :rtype: InMemorySaver | PostgresSaver | RedisSaver | MongoDBSaver
    """

    
    memory_saver = None

    if api_settings.SHORT_TERM_MEMORY:
        if api_settings.SHORT_TERM_MEMORY["type"].lower() == "redis":
            redis_url = api_settings.SHORT_TERM_MEMORY["url"]
            redis_client = redis.Redis.from_url(redis_url, decode_responses=True)
            memory_saver = RedisSaver(redis_client=redis_client)
            memory_saver.setup()

        elif api_settings.SHORT_TERM_MEMORY["type"].lower() == "postgres":
            postgres_url = api_settings.SHORT_TERM_MEMORY["url"]

            min_pool_size = api_settings.SHORT_TERM_MEMORY["options"]["min_pool_size"] or 5
            max_pool_size = api_settings.SHORT_TERM_MEMORY["options"]["max_pool_size"] or 20

            pool = ConnectionPool(
                conninfo=postgres_url,
                min_size=min_pool_size,
                max_size=max_pool_size,
                kwargs={
                    "autocommit": True,
                    "row_factory": psycopg.rows.dict_row
                }
            )
            memory_saver = PostgresSaver(conn=pool)
            memory_saver.setup()

        elif api_settings.SHORT_TERM_MEMORY["type"].lower() == "mongodb":
            mongodb_url = api_settings.SHORT_TERM_MEMORY["url"]

            # TODO: set minimum and maximum of pool size
            mongo_client = MongoClient(
                mongodb_url
            )

            memory_saver = MongoDBSaver(client=mongo_client)
        
        else:
            # TODO: handle exception
            ...
    else:
        memory_saver = MemorySaver()

    return memory_saver



def chat_node(state:MessagesState):
    
    if system_prompt_template:
        messages = system_prompt_template.invoke(state)
    else:
        messages = state["messages"]

    response = api_settings.LLM_MODEL.invoke(messages)

    return {"messages": response}


tool_node = ToolNode(api_settings.TOOLS)

graph = StateGraph(MessagesState)
graph.add_node("chat", chat_node)
graph.add_node("tools", tool_node)

graph.add_conditional_edges(
    "chat",
    tools_condition
)

graph.add_edge(START, "chat")
graph.add_edge("tools", "chat")
graph.add_edge("chat", END)

compiled_graph = graph.compile(checkpointer=generate_short_term_memory())


