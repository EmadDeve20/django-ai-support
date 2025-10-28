from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema

from .serializers import InputOutputChatSerializer
from .backends import normal_chat_with_ai

class BaseApi(APIView):

    @property
    def thread_id(self):
        return self.request.session.session_key


class ChatAiSupportApi(BaseApi):

    @extend_schema(
        tags=["Django AI Support"],
        request=InputOutputChatSerializer,
        responses=InputOutputChatSerializer
    )
    def post(self, request):
        
        serializer = InputOutputChatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ai_response = normal_chat_with_ai(serializer.validated_data["message"],
                                          thread_id=self.thread_id)
        
        return Response(InputOutputChatSerializer({"message": ai_response}).data)



class AuthChatAiSupportApi(ChatAiSupportApi):

    permission_classes = (IsAuthenticated,)

    @property
    def thread_id(self):
        return self.request.user.id

