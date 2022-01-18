
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
class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
         
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        profile=ProfileSerializer(Profile.objects.filter(user=user).first()).data
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'profile':profile,
        })
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
    
