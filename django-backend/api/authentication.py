from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from api.models import CustomToken

class CustomTokenAuthentication(TokenAuthentication):
    model = CustomToken  # CustomToken 모델 사용

    def authenticate(self, request):
        print(f"Authentication header: {request.headers.get('Authorization')}")
        return super().authenticate(request)

    def authenticate_credentials(self, key):
        print(f"Authenticating token: {key}")
        try:
            token = self.model.objects.select_related('user').get(key=key)
        except self.model.DoesNotExist:
            raise AuthenticationFailed('Invalid token.')

        if not token.user.is_active:
            raise AuthenticationFailed('User is inactive or deleted.')

        return (token.user, token)

class DebugTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization', None)
        print(f"Authenticate called with header: {auth_header}")  # 디버깅용 로그
        return super().authenticate(request)

    def authenticate_credentials(self, key):
        print(f"Authenticating credentials for key: {key}")
        return super().authenticate_credentials(key)
