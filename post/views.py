from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from post.models import Post, Image
from post.serializers import ImageSerializer, PostCreateSerializer

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
            # print(serializer.data)
            # print(serializer.data['image'])
            return Response({"message":"이미지 변환 완료", "post_img" : serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"message":"이미지를 등록해주세요"}, status=status.HTTP_400_BAD_REQUEST)


class PostView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        """게시물을 생성합니다."""
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            # print(serializer.data)
            return Response({"message":"게시물 생성 완료"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, post_id):
        """post_id를 받아 특정 게시물을 삭제합니다."""
        post = get_object_or_404(Post, id=post_id)
        if request.user == post.author:
            post.delete()
            image = post.post_img
            image.delete()
            return Response({"message":"게시물 삭제 완료"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message":"삭제 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

class PostLikeView(APIView):
    def post(self, request, post_id):
        """post_id를 받아 특정 게시물을 좋아요 합니다."""