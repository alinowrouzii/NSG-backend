from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.viewsets import mixins
from knox.auth import TokenAuthentication
from rest_framework.pagination import LimitOffsetPagination
from chatroom.api.serializers import MessageSerializer
from chatroom.models import Message
class MessageAPIView(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = MessageSerializer
    pagination_class = LimitOffsetPagination
    
    def get_queryset(self):
        if self.is_admin():
            return Message.objects.all().order_by("-timestamp")
        
        return Message.objects.filter(user=self.request.user).order_by("-timestamp")

    def is_admin(self):
        # TODO: it can be changed to superadmin
        return IsAdminUser().has_permission(self.request, view=None)
        
    def set_request_context(self):
        request = self.request
        
        user = None
        user_is_sender = True
        
        if self.is_admin():
            user = request.data["user"]
            # If admin wants to send message to user, user_is_sender should be False
            user_is_sender = False
        else:
            user = request.user.id
             
        mutable = request.data._mutable
        request.data._mutable = True
        request.data['user'] = user
        request.data['user_is_sender'] = user_is_sender
        request.data._mutable = mutable
        
    def post(self, request, *args, **kwargs):
        self.set_request_context()
        return super().create(request, *args, **kwargs)