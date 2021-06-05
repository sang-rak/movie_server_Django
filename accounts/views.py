from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer, UserinfoSerializer
from .models import User
from django.shortcuts import get_list_or_404
import requests
@api_view(['POST'])
def signup(request):
	#1-1. Client에서 온 데이터를 받아서
    password = request.data.get('password')
    password_confirmation = request.data.get('passwordConfirmation')
		
	#1-2. 패스워드 일치 여부 체크
    if password != password_confirmation:
        return Response({'error': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
		
	#2. UserSerializer를 통해 데이터 직렬화
    serializer = UserSerializer(data=request.data)
    
	#3. validation 작업 진행 -> password도 같이 직렬화 진행
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        url = "https://dapi.kakao.com/v2/vision/face/detect"
        MYAPP_KEY = '6d1b396afbe3b40debd197b90f56c75e'
        headers = {'Authorization': 'KakaoAK {}'.format(MYAPP_KEY)}
        filename = './media/'+str(user)+'.png'

        files = { 'image' : open(filename, 'rb')}

        response = requests.post(url, headers=headers, files=files)
        result = response.json()

        male = result['result']['faces'][0]['facial_attributes']['gender']['male']
        age = result['result']['faces'][0]['facial_attributes']['age']
        #4. 비밀번호 해싱 후 
        user.set_password(request.data.get('password'))
        user.male = male
        user.age = age
        user.save()
    # password는 직렬화 과정에는 포함 되지만 → 표현(response)할 때는 나타나지 않는다.
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(["GET"])
def userinfo(request):
    if request.method == "GET":
        userinfo = get_list_or_404(User)
        serializer = UserinfoSerializer(userinfo, many=True)
        return Response(serializer.data)

