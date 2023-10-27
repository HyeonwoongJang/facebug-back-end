from rest_framework import serializers
import re
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from user.models import User
from rest_framework import status

def validate_password(password, password_confirmation):
    validate_password_strength(password)
    """보안을 위해 프론트에서 한번하고 백단에서 검증을 한번 더 거치는게 좋다"""
    if password != password_confirmation:
        raise serializers.ValidationError({"password_confirmation": "비밀번호와 비밀번호 확인이 일치하지 않습니다."})
    


def validate_password_strength(password):
    pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[a-zA-Z]).{8,20}$"
    if not re.match(pattern, password):
        msg = "적어도 8글자 20글자이하 및 대문자, 소문자, 숫자가 하나씩은 들어가있어야하며, 특수문자 입력이 가능합니다."
        raise serializers.ValidationError({"password": msg})

def is_password_same_as_previous(old_password, new_password, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.check_password(old_password):
        print(user.check_password(old_password))
        if old_password==new_password:
            raise serializers.ValidationError({"password_duplicated": "비밀번호가 전과 같습니다. 다시 시도하여주십시오"})
    else:
        raise serializers.ValidationError({"password_check": "현재 비밀번호와 일치하지 않습니다."})