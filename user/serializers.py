from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import serializers
from user.models import User, ProfileImage
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    """회원가입 페이지, 회원 정보 수정 페이지에서 사용되는 시리얼라이저입니다."""

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        # user = super().create(validated_data)
        password=validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        if self.context['profile_img']:
            profile_img = self.context['profile_img']
            image_data=profile_img.get('profile_img')
            ProfileImage.objects.create(owner=user, profile_img=image_data)
            return user
        else:
            profile_img = settings.DEFAULT_PROFILE_IMAGE
            ProfileImage.objects.create(owner=user, profile_img=profile_img)
            return user

class LoginSerializer(TokenObtainPairSerializer):
    """DRF의 JWT 로그인 방식에 사용되는 TokenObtainPairSerializer를 상속하여 Serializer를 커스터마이징하여 재정의합니다."""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, request_data):
        print(request_data)
        request_email = request_data.get('email')
        request_password = request_data.get('password')

        try:
            user = User.objects.get(email=request_email)
        except User.DoesNotExist:
            raise AuthenticationFailed("사용자를 찾을 수 없습니다. 로그인 정보를 확인하세요.")

        if not user.check_password(request_password):
            raise AuthenticationFailed("비밀번호가 일치하지 않습니다.")
        elif user.is_active == False:
            raise AuthenticationFailed("이메일 인증이 필요합니다.")
        
        token = super().get_token(user)
        refresh = RefreshToken.for_user(user)
        
        user_profile_img = ProfileImage.objects.get(owner=user)
        token['nickname'] = user.nickname
        token['profile_img'] = str(user_profile_img.profile_img)
        token['intro'] = user.intro
        
        return {
            'access': str(token.access_token),
            'refresh': str(refresh)
        }