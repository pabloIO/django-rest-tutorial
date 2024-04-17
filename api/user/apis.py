from rest_framework import views, exceptions, permissions, response
from .serializer import UserSerializer
from .services import create_user, user_email_selector, create_token
from .authentication import CustomUserAuthentication

class RegisterApi(views.APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        serializer.instance = create_user(user_dc=data)

        print(data)
        print(data.first_name)

        return response.Response(serializer.data)

class LoginApi(views.APIView):
    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]

        user = user_email_selector(email)

        if user is None:
            raise exceptions.AuthenticationFailed("Invalid credentials")

        if not user.check_password(raw_password=password):
            raise exceptions.AuthenticationFailed("Invalid credentials")

        token = create_token(user_id=user.id)

        resp = response.Response()

        resp.set_cookie(key="jwt", value=token, httponly=True)

        return resp
    
class UserApi(views.APIView):

    authentication_classes = (CustomUserAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        user = request.user

        serializer = UserSerializer(user)

        return response.Response(serializer.data)

class LogoutApi(views.APIView):

    authentication_classes = (CustomUserAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        resp = response.Response()
        resp.delete_cookie("jwt")
        resp.data = {"message": "Goodbye..."}
        
        return resp