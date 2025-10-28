from rest_framework.permissions import IsAuthenticated

from .views import AuthChatAiSupportApi, ChatAiSupportApi


def create_chat_api(added_classes:list=[], **kwargs) -> ChatAiSupportApi:
    """
    Create a dynamically ChatAiSupportApi class.


    Args:
        added_classes (list, optional): more classes if you want to inherit from. Defaults to [].

    Returns:
        ChatAiSupportApi: return the created Dynamic ChatAiSupportApi class
    """

    class_name = "DynamicChatAiSupportApi"

    return type(class_name, (ChatAiSupportApi, *added_classes), **kwargs)


def create_authenticated_chat_api(permission_classes:tuple=(IsAuthenticated,), 
authentication_classes:list=[],
added_classes:list=[], **kwargs) -> AuthChatAiSupportApi:
    """
    Create a dynamically AuthChatAiSupportApi class.
    

    Args:
        permission_classes (tuple, optional): permission classes for AuthChatAiSupportApi. Defaults to (IsAuthenticated,).
        authentication_classes (list, optional): authentication classes for AuthChatAiSupportApi. Defaults to [].
        added_classes (list, optional): more classes if you want to inherit from. Defaults to [].

    Returns:
        AuthChatAiSupportApi: return the created Dynamic ChatAiSupportApi class
    """
   
    class_variables = {
        "permission_classes": permission_classes,
        "authentication_classes": authentication_classes,
        **kwargs
    }    

    class_name = "DynamicAuthChatAiSupportApi"

    return type(class_name, (AuthChatAiSupportApi,*added_classes), class_variables) 
