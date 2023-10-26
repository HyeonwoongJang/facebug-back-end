from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import serializers
from user.models import User, ProfileImage
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from user.common_utils import validate_password, is_password_same_as_previous
from rest_framework.validators import UniqueValidator
# from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    """회원가입 페이지, 회원 정보 수정 페이지에서 사용되는 시리얼라이저입니다."""

    password = serializers.CharField(write_only=True, required=True)
    password_confirmation = serializers.CharField(write_only=True) 
    profile_img = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = "__all__"
        
    def get_profile_img(self, user):
        profile_img = ProfileImage.objects.filter(owner=user).first()
        if profile_img:
            return profile_img.profile_img.url  # 이미지 URL 반환
        return settings.DEFAULT_PROFILE_IMAGE   

    # def get_profile_img(self, user):
    #     profile_img = ProfileImage.objects.get(owner=user)
    #     if profile_img:
    #         return str(profile_img.profile_img)
    #     else:
    #         profile_img = settings.DEFAULT_PROFILE_IMAGE
    #     return profile_img
    
    def validate(self, data):
        password = data.get("password")
        password_confirmation = data.get("password_confirmation")
        if password and password_confirmation:
            validate_password(password, password_confirmation)
        return data
    
    def create(self, validated_data):
        # user = super().create(validated_data)
        validated_data.pop("password_confirmation")
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
        
    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        
        profile_img = self.context["profile_img"]
        print(profile_img)
        if profile_img:
            image_data = profile_img.get('profile_img')
            ProfileImage.objects.get(owner=user).delete()
            ProfileImage.objects.create(owner=user, profile_img=image_data)
            return user
        else:
            ProfileImage.objects.create(owner=user, profile_img=settings.DEFAULT_PROFILE_IMAGE)
            return user
class PasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    new_password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("old_password","new_password","new_password_confirm")

    def validate(self, data):
        user_id = self.context.get("user_id")
        old_password = data.get("old_password")
        new_password = data.get("new_password")
        is_password_same_as_previous(old_password, new_password, user_id)
        new_password_confirm = data.get("new_password_confirm")
        validate_password(new_password, new_password_confirm)
        return data

    def update(self, instance, validated_data):
        validated_data.pop("old_password")
        validated_data.pop("new_password_confirm")
        new_password = validated_data.pop("new_password", None)
        if new_password:
            instance.set_password(new_password)
            instance.save()
        return instance

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
            'message': "로그인 성공",
            'access': str(token.access_token),
            'refresh': str(refresh)
        }