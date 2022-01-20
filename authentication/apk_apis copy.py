
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .repo import ProfileRepo
from .serializers import ProfileSerializer
from django.http import JsonResponse
from core.constants import SUCCEED,FAILED


 
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import Profile


# class EditProfile(ObtainAuthToken):
#     def post(self,request,*args, **kwargs):
#         context={'result':FAILED}
#         profile_id=0
#         request=ProfileRepo(request=request).login_by_token()
#         if 'profile_id' in kwargs:
#             profile_id=kwargs['profile_id']
#         serializer = self.serializer_class(data=request.data,
#                                            context={'request': request})
#         serializer.is_valid(raise_exception=True)

#                 # profile_id=edit_profile_form.cleaned_data['profile_id']
#         first_name=serializer.validated_data['first_name']
#         last_name=serializer.validated_data['last_name']
#         email=serializer.validated_data['email']
#         bio=serializer.validated_data['bio']
#         mobile=serializer.validated_data['mobile']
#         address=serializer.validated_data['address']
#         result=ProfileRepo(request=request).edit_profile(profile_id=profile_id,
#         first_name=first_name,
#         last_name=last_name,
#         email=email,
#         bio=bio,
#         mobile=mobile,
#         address=address,
#         )
#         if result:
#             context['result']=SUCCEED
#         return JsonResponse(context)    

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        username=(request.data['username'])
        password=(request.data['password'])
        ProfileRepo(request=request).login(request,username=username,password=password)
        # serializer = self.serializer_class(data=request.data,
        #                                    context={'request': request})
        # serializer.is_valid(raise_exception=True)
        if request is None:
            context={

            }
        else:
            user =request.user
            token, created = Token.objects.get_or_create(user=user)
            profile=ProfileSerializer(Profile.objects.filter(user=user).first()).data
            context={
                'token': token.key,
                'user_id': user.pk,
                'email': user.email,
                'profile':profile,
            }
        return Response(context)
 