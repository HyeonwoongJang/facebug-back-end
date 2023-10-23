from django.conf import settings
from rest_framework.exceptions import NotFound, AuthenticationFailed
from rest_framework import serializers
from user.models import User, ProfileImage
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

        if self.context['profile_img']:
            profile_img = self.context['profile_img']
            # print(profile_img)
            for image_data in profile_img.getlist('profile_img'):
                # print(image_data)
                ProfileImage.objects.create(owner=user, profile_img=image_data)
            return user
        else:
            profile_img = settings.DEFAULT_PROFILE_IMAGE
            ProfileImage.objects.create(owner=user, profile_img=profile_img)
            return user
        
class LoginSerializer(TokenObtainPairSerializer):
    """DRF의 JWT 로그인 방식에 사용되는 TokenObtainPairSerializer를 상속하여 Serializer를 커스터마이징하여 재정의합니다."""
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        user_profile_img = ProfileImage.objects.get(owner=user)
        token['profile_img'] = str(user_profile_img.profile_img)

        return token