from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from user.models import User
from user.serializers import UserSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status


class RegisterView(APIView):
    def post(self, request):
        """사용자 정보를 받아 회원가입 합니다."""
        serializer = UserSerializer(data=request.data, context={'profile_img':request.FILES})
        print(request.FILES)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'회원가입 성공'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class EmailCheckView(APIView):
    def post(self, request):
        """이메일 중복 검사를 위한 클래스 뷰입니다."""
        email = User.objects.filter(email=request.data['email'])
        # print(request.data['email'])
        # print(email)
        if email : 
            return Response({'message':'해당 이메일은 이미 사용 중입니다.'}, status=status.HTTP_409_CONFLICT)
        else:
            return Response({'message':'해당 이메일은 사용 가능합니다.'}, status=status.HTTP_200_OK)

class NicknameCheckView(APIView):
    def post(self, request):
        """닉네임 중복 검사를 위한 클래스 뷰입니다."""
        nickname = User.objects.filter(nickname=request.data['nickname'])
        # print(request.data['nickname'])
        # print(nickname)
        if nickname :
            return Response({'message':'해당 닉네임은 이미 사용 중입니다.'}, status=status.HTTP_409_CONFLICT)
        else:
            return Response({'message':'해당 닉네임은 사용 가능합니다.'}, status=status.HTTP_200_OK)

class LoginView(TokenObtainPairView):
        """
        사용자 정보를 받아 로그인 합니다.
        DRF의 JWT 토큰 인증 로그인 방식에 기본 제공된는 클래스 뷰를 커스터마이징하여 재정의합니다.
        """
        serializer_class = LoginSerializer

class UserInfoView(APIView):
    def get(self, request, user_id):
        """사용자의 회원 정보를 보여줍니다."""
    
    def put(self, request, user_id):
        """사용자의 정보를 받아 회원 정보를 수정합니다."""
    
    def patch(self, request, user_id):
        """사용자의 비밀번호를 수정합니다."""