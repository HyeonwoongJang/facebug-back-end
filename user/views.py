from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from user.models import User
from user.serializers import UserSerializer, LoginSerializer,PasswordSerializer
from rest_framework.response import Response
from rest_framework import status,permissions

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from .tasks import send_verification_email

class RegisterView(APIView):
    def post(self, request):
        """사용자 정보를 받아 회원가입 합니다."""
        
        serializer = UserSerializer(data=request.data, context={'profile_img':request.FILES})
        
        if serializer.is_valid():
            user = serializer.save()
            
            # 이메일 확인 토큰 생성
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # 이메일에 인증 링크 포함하여 보내기
            verification_url = f"http://127.0.0.1:8000/verify-email/{uid}/{token}/"
            
            send_verification_email.delay(user.id, verification_url, user.email)                        # 'delay' : Celery 작업을 예약하여 나중에 실행되도록 하는 메소드입니다. 'delay' 메소드를 호출하면 작업이 백그라운드에서 비동기적으로 실행됩니다.
            
            return Response({'message':'회원가입 성공'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(APIView):
    """사용자가 받은 이메일에 인증 링크를 눌렀을 때 사용자에게 권한 부여를 진행합니다."""
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
        DRF의 JWT 토큰 인증 로그인 방식에 기본 제공되는 클래스 뷰를 커스터마이징하여 재정의합니다.
        """
        serializer_class = LoginSerializer

class UserInfoView(APIView):
    permission_classes = [permissions.IsAuthenticated]
        
    def get_user(self, user_id):
        return get_object_or_404(User, id=user_id)

    def get(self, request, user_id):
        """사용자의 회원 정보를 보여줍니다."""
        serializer = UserSerializer(self.get_user(user_id))
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, user_id): 
        """사용자의 정보를 받아 회원 정보를 수정합니다."""
        serializer = UserSerializer(
            self.get_user(user_id),
            data=request.data,
            context={"profile_img": request.FILES, "user_id": user_id},
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "회원정보를 수정할 수 없습니다.", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
            
    def put(self, request, user_id):
        """사용자의 비밀번호만을 수정합니다."""
        serializer = PasswordSerializer(
            self.get_user(user_id),
            context={"user_id": user_id},
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "비밀번호를 수정 하였습니다."},status=status.HTTP_200_OK,)
        else:
            return Response(
                {"message": "비밀번호를 수정 할 수 없습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )