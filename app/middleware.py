from jose import jwt
from environs import Env
from .models import  CustomUser
from django.http.response import JsonResponse

def verify_token(request):

    try:
        token = request.headers.get('x-access-token')
        env = Env()
        env.read_env()
        secret_key = env("JWT_SECRET_KEY")

        if(token == None):
            return { 'success': False,'message': "usuario no autorizado."}

        user_jwt = jwt.decode(token, secret_key, algorithms=["HS256"])
        
        if(user_jwt == None):
           return { 'success': False,'message': "usuario no autorizado."}
        try:
            return  { 'success': True, "user": CustomUser.objects.get( id=user_jwt['id'])}
            
        except :
           return { 'success': False,'message': "usuario no autorizado."}
    except :
       return { 'success': False,'message': "usuario no autorizado."}

# from django.utils.functional import SimpleLazyObject
# from django.utils.deprecation import MiddlewareMixin
# from django.contrib.auth.models import AnonymousUser, User
# from django.conf import LazySettings
# from django.contrib.auth.middleware import get_user
# import jwt
# import traceback

# settings = LazySettings()

# class JWTAuthenticationMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         request.user = SimpleLazyObject(lambda: self.__class__.get_jwt_user(request))

#     @staticmethod
#     def get_jwt_user(request):

#         user_jwt = get_user(request)
#         if user_jwt.is_authenticated():
#             return user_jwt
#         token = request.META.get('HTTP_AUTHORIZATION', None)
#         print('token:')
#         print(token)
#         user_jwt = AnonymousUser()
#         if token is not None:
#             try:
#                 user_jwt = jwt.decode(
#                     token,
#                     settings.WP_JWT_TOKEN,
#                 )
#                 print(user_jwt)
#                 user_jwt = User.objects.get(
#                     id=user_jwt['data']['user']['id']
#                 )
#             except Exception as e: # NoQA
#                 traceback.print_exc()
#         return user_jwt