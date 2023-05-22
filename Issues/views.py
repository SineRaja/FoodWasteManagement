from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .models import Issue
from .serializers import IssueSerializer


class IssueCreateList(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    def post(self, request, *args, **kwargs):
        request.data["created_by"] = request.user.id
        request.data['user_type'] = request.user.user_type
        response = super().post(request, args, kwargs)
        response.data = {
            "id": response.data["id"]
        }
        return response
