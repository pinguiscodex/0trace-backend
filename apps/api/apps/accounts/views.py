from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from apps.common.api.responses import ok
from apps.common.api.serializers import EmptySerializer

from .serializers import LoginSerializer, SignupSerializer
from .services.auth_service import login_failed, login_user, logout_user, signup_user
from .services.session_service import session_context


class CSRFView(APIView):
    permission_classes = [AllowAny]
    serializer_class = EmptySerializer

    @extend_schema(tags=["auth"], responses={200: dict})
    def get(self, request):
        return ok({"csrf_token": get_token(request)})


@method_decorator(csrf_exempt, name="post")
class SignupView(APIView):
    permission_classes = [AllowAny]
    serializer_class = SignupSerializer

    @extend_schema(
        tags=["auth"],
        request=SignupSerializer,
        responses={201: dict},
        examples=[OpenApiExample("Signup", value={"handle": "tracepilot", "email": "trace@example.com", "password": "correct horse battery", "terms_accepted": True})],
    )
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = signup_user(request=request, **serializer.validated_data)
        return ok(session_context(user), status_code=201)


@method_decorator(csrf_exempt, name="post")
class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    @extend_schema(tags=["auth"], request=LoginSerializer, responses={200: dict})
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            login_failed(request=request, identifier=request.data.get("identifier", ""))
            serializer.is_valid(raise_exception=True)
        login_user(request=request, user=serializer.validated_data["user"])
        return ok(session_context(serializer.validated_data["user"]))


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmptySerializer

    @extend_schema(tags=["auth"], responses={200: dict})
    def post(self, request):
        logout_user(request=request)
        return ok({"logged_out": True})


class SessionView(APIView):
    permission_classes = [AllowAny]
    serializer_class = EmptySerializer

    @extend_schema(tags=["auth"], responses={200: dict})
    def get(self, request):
        return ok(session_context(request.user))
