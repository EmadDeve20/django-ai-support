from redis.exceptions import ConnectionError as RedisConnectionError
from psycopg2 import OperationalError as PostgresConnectionError
from pymongo.errors import ConnectionFailure as MongodbConnectionError
from pymongo.errors import ServerSelectionTimeoutError

from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from langchain_core.messages import HumanMessage


from .graphs import compiled_graph

def normal_chat_with_ai(user_message:str, thread_id:str) -> str:
    """
    function to chat with AI

    Args:
        user_message (str): message of user
        thread_id (str): id of thread to save messages

    Returns:
        str: return coming message
    """


    config = {"configurable": {"thread_id": str(thread_id)}}

    messages = [
        HumanMessage(user_message)
    ]

    try:
        ai_response = compiled_graph.invoke({"messages": messages}, config=config)

    except RedisConnectionError:
        raise ValidationError(_("AI support is not available right now!"))

    except PostgresConnectionError:
        raise ValidationError(_("AI support is not available right now!"))

    except MongodbConnectionError:
        raise ValidationError(_("AI support is not available right now!"))

    except ServerSelectionTimeoutError:
        raise ValidationError(_("AI support is not available right now!"))

    except Exception:
        raise ValidationError(_("AI support is not available right now!"))

    ai_response = ai_response["messages"][-1].content

    return ai_response

