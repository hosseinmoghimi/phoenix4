
from django.http import Http404
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .repo import ProfileRepo
from .serializers import ProfileSerializer
from django.http import JsonResponse
from core.constants import SUCCEED,FAILED



from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import Profile



class RegisterProfile(APIView):

    def post(self,request,*args, **kwargs):
        
            
        from log.repo import LogRepo
        LogRepo(request=request).add_log(title="Http404 authentication api views")
        raise Http404
        result=FAILED
        context={'result':FAILED}

            # profile_id=edit_profile_form.cleaned_data['profile_id']
        first_name=request.data['first_name']
        last_name=request.data['last_name']
        email=request.data['email']
        bio=request.data['bio']
        mobile=request.data['mobile']
        address=request.data['address']
        result1=ProfileRepo(request=request).add_profile(first_name=first_name,
        last_name=last_name,
        email=email,
        bio=bio,
        mobile=mobile,
        address=address,
        )
        if result1:
            result=SUCCEED
            context['result']=SUCCEED
            profile=Profile.objects.filter(user=request.user).first()
            if profile is not None:
                context={
                    'result':result,
                    'user_id': profile.user.pk,
                    'email': profile.user.email,
                    'profile':ProfileSerializer(Profile.objects.filter(user=request.user).first()).data,
                }
                ProfileRepo(request=request).logout()
            return JsonResponse(context)




class EditProfile(APIView):
    def post(self,request,*args, **kwargs):
        result=FAILED
        context={'result':FAILED}
        profile_id=0
        request=ProfileRepo(request=request).login_by_token()

        if 'profile_id' in kwargs:
            profile_id=kwargs['profile_id']
        
        if request is not None:

                # profile_id=edit_profile_form.cleaned_data['profile_id']
            first_name=request.data['first_name']
            last_name=request.data['last_name']
            email=request.data['email']
            bio=request.data['bio']
            mobile=request.data['mobile']
            address=request.data['address']
            result1=ProfileRepo(request=request).edit_profile(profile_id=profile_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            bio=bio,
            mobile=mobile,
            address=address,
            )
        if result1:
            result=SUCCEED
            context['result']=SUCCEED
            profile=Profile.objects.filter(user=request.user).first()
            if profile is not None:
                context={
                    'result':result,
                    'user_id': profile.user.pk,
                    'email': profile.user.email,
                    'profile':ProfileSerializer(Profile.objects.filter(user=request.user).first()).data,
                }
                ProfileRepo(request=request).logout()
        return JsonResponse(context)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        result=FAILED
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        profile=ProfileSerializer(Profile.objects.filter(user=user).first()).data
        context={
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'profile':profile,
            'result':result,
        }
        ProfileRepo(request=request).logout()
        return Response(context)
@csrf_exempt
class ProfileApi(APIView):
    
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [AllowAny]

    def login(self,request,*args, **kwargs):
        context={}
        if request.method=='GET':
            print(request.session)
            print(100*"#@$")
            token=request.session.csrf_token
            context['token']=token
            context['result']=SUCCEED
            return JsonResponse(context)
        if request.method=='POST':

            print(100*"#@$")
            
            context['result']=FAILED
            # if request.method=='POST':
            username=request.data['username']
            password=request.data['password']
            print(username)
            print(password)
            profile=ProfileRepo(request=request).login(request,username,password)
            profile=ProfileRepo(request=request).me
            if profile is not None:
                context['profile']=ProfileSerializer(profile).data
                context['result']=SUCCEED
            return JsonResponse(context)
    
