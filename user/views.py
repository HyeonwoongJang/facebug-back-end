from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from user.models import User
from user.serializers import UserSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail

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


class SendVerificationEmailView(APIView):
    def post(self, request):
            
            user = User.objects.get(email=request.data['email'])

            # 이메일 확인 토큰 생성
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # 이메일에 확인 링크 포함하여 보내기
            verification_url = f"http://127.0.0.1:8000/verify-email/{uid}/{token}/"
            # 이메일 전송 코드 작성 및 이메일에 verification_url을 포함하여 보내기

            # 이메일 전송
            subject = '이메일 확인 링크'
            message = f'이메일 확인을 완료하려면 다음 링크를 클릭하세요: {verification_url}'
            from_email = 'hyeonwoongjang01@gmail.com'
            recipient_list = [user.email]

            send_mail(subject, message, from_email, recipient_list)

            return Response(status = status.HTTP_200_OK)
    
class VerifyEmailView(APIView):
    def get(self, request, uidb64, token):
        # uidb64와 token을 사용하여 사용자 확인
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(id=uid)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
        return Response(status=status.HTTP_200_OK)

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