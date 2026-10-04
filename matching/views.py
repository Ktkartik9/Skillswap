from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .services import get_matches
from .serializers import MatchUserSerializer


User = get_user_model()


class MatchListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        match_ids = get_matches(
            request.user
        )

        users = User.objects.filter(
            id__in=match_ids
        )

        serializer = MatchUserSerializer(
            users,
            many=True
        )

        return Response(
            serializer.data
        )