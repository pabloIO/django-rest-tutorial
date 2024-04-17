from rest_framework import views, response, exceptions, permissions
from user import authentication
from .serializer import StatusSerializer
from rest_framework import status as rest_status
from .services import create_status, get_user_statuses, get_user_status_detail, delete_user_status, update_user_status

class StatusCreateListApi(views.APIView):
    authentication_classes = (authentication.CustomUserAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        serializer = StatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        # create a status
        serializer.instance = create_status(user=request.user, status=data)

        return response.Response(data=serializer.data)

    def get(self, request):
        status_collection = get_user_statuses(user=request.user)
        serializer = StatusSerializer(status_collection, many=True)
        return response.Response(data=serializer.data)


class StatusRetrieveUpdateDeleteApi(views.APIView):
    authentication_classes = (authentication.CustomUserAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, status_id):
        status_detail = get_user_status_detail(status_id=status_id)
        serializer = StatusSerializer(status_detail)
        return response.Response(data=serializer.data)

    def put(self, request, status_id):
        serializer = StatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        status = serializer.validated_data
        # create a status
        serializer.instance = update_user_status(user=request.user, status_id=status_id, status_data=status)

        return response.Response(data=serializer.data, status=rest_status.HTTP_202_ACCEPTED)

    def delete(self, request, status_id):
        delete_user_status(request.user, status_id=status_id)

        return response.Response(status=rest_status.HTTP_204_NO_CONTENT)

    