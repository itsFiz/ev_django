from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from knox.auth import AuthToken
from users.models import User

class CustomAuthentication(TokenAuthentication):

    def authenticate(self, request):
        try:
            
            token = request.META.get('HTTP_AUTHORIZATION')
            if token:
                t = token.partition(" ")
                token = t[-1]

            if not token:
                return None

            token = token[:8]

            token_data = AuthToken.objects.filter(token_key=token).first() 

            user = token_data.user

            return (user, None)

        except Exception as e:
            print(e)
            return AuthenticationFailed()