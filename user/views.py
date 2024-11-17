from user.serializers import UserSerializer, AuthTokenSerializer
from rest_framework import generics, authentication, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer

class UpdateUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class ListUsersView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    @method_decorator(cache_page(60 * 60))
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(status=200, data=serializer.data)

class DeleteUserView(generics.DestroyAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)


class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
