from langgraph.graph import START, END, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langgraph.checkpoint.memory import MemorySaver
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


def init_agent():
    """
    initialize agent
    """

    def chat_node(state:MessagesState):
        
        if system_prompt_template:
            messages = system_prompt_template.invoke(state)
        else:
            messages = state["messages"]

        response = api_settings.LLM_MODEL.invoke(messages)

        return {"messages": response}


    def short_term_memory_from_settings():
        
        memory_saver = None

        # TODO: add Validation to check memory saver is None or not
        if api_settings.SHORT_TERM_MEMORY.type.lower() == "redis":
            memory_saver = RedisSaver
        
        elif api_settings.SHORT_TERM_MEMORY.type.lower() == "postgres":
            memory_saver = PostgresSaver
        
        elif api_settings.SHORT_TERM_MEMORY.type.lower() == "mongodb":
            memory_saver = MongoDBSaver

        with memory_saver.from_conn_string(api_settings.SHORT_TERM_MEMORY.url) as checkpointer:

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

            compiled_graph = graph.compile(checkpointer=checkpointer)

            return compiled_graph
    

    def default_short_term_memory():

        tool_node = ToolNode(api_settings.TOOLS)

        memory = MemorySaver()

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

        compiled_graph = graph.compile(checkpointer=memory)

        return compiled_graph


    if api_settings.SHORT_TERM_MEMORY is None:
        return default_short_term_memory()
    
    return short_term_memory_from_settings()


