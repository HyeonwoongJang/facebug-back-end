from rest_framework import serializers
from user.models import User

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