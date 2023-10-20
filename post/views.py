from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from post.models import Post, Image
from post.serializers import ImageSerializer

class PostListView(APIView):
    def get(self, request, user_id=None):
        """
        user_id가 없을 경우 모든 계시물을 Response 합니다.
        user_id가 있을 경우 특정 유저의 게시물을 Response 합니다.
        """

class ImageConvertView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        """이미지를 받아 변환시킵니다."""

        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # print(serializer.data['image'])
            return Response({"message":"이미지 변환 완료", "post_img" : serializer.data['image']}, status=status.HTTP_201_CREATED)
        return Response({"message":"이미지를 등록해주세요"}, status=status.HTTP_400_BAD_REQUEST)


class PostView(APIView):
    def post(self, request):
        """게시물을 생성합니다."""
    
    def delete(self, request, post_id):
        """post_id를 받아 특정 게시물을 삭제합니다."""


class PostLikeView(APIView):
    def post(self, request, post_id):
        """post_id를 받아 특정 게시물을 좋아요 합니다."""