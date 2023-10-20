from rest_framework import serializers
from user.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    """회원가입 페이지, 회원 정보 수정 페이지에서 사용되는 시리얼라이저입니다."""
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        user = super().create(validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user

class LoginSerializer(TokenObtainPairSerializer):
    """DRF의 JWT 로그인 방식에 사용되는 TokenObtainPairSerializer를 상속하여 Serializer를 커스터마이징하여 재정의합니다."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # print(user.profile_img)
        # print(user.profile_img.url)
        
        token['profile_img'] = user.profile_img.url

        return token