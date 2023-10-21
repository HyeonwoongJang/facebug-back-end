from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from post.models import Post, Comment
from post.serializers import ImageSerializer, PostCreateSerializer, PostListSerializer, CommentSerializer

class PostListView(APIView):
    def get(self, request, user_id=None):
        """
        user_id가 없을 경우 모든 계시물을 Response 합니다.
        user_id가 있을 경우 특정 유저의 게시물을 Response 합니다.
        """
        if user_id is None:
            all_posts = Post.objects.all().order_by('-created_at')
            serializer = PostListSerializer(all_posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            user_posts = Post.objects.filter(author=user_id).order_by('-created_at')
            serializer = PostListSerializer(user_posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

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
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, post_id):
        """like / unlike 기능입니다."""
        post = Post.objects.get(id=post_id)
        me = request.user
        if me in post.like.all():
            post.like.remove(me)
            return Response({"message":"unlike"}, status=status.HTTP_204_NO_CONTENT)
        else:
            post.like.add(me)
            return Response({"message":"like"}, status=status.HTTP_201_CREATED)
        
class CommentView(APIView):
    """
    comment_id가 없을 경우 댓글을 조회하거나 생성합니다.
    comment_id가 있을 경우 삭제합니다.
    """
    def post(self, request, post_id):
        """특정 게시물에 댓글을 생성합니다."""
        if request.user :
            serializer = CommentSerializer(data=request.data)
            # print(request.data)
            if serializer.is_valid():
                post = Post.objects.get(id=post_id)
                serializer.save(author=request.user, post=post)
                # print(serializer.data)
                return Response({"message":"댓글 등록 완료"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else :
            return Response({"message":"로그인이 필요한 요청입니다."}, status=status.HTTP_401_UNAUTHORIZED)
        
    def get(self, request, post_id):
        """특정 게시물에 작성된 모든 댓글을 불러옵니다."""
        post = Post.objects.get(id=post_id)
        comments = Comment.objects.filter(post=post).order_by('-id')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, post_id, comment_id):
        """특정 댓글을 삭제합니다."""
        if request.user:
            comment = Comment.objects.get(id=comment_id)
            if request.user == comment.author :
                comment.delete()
                return Response({"message":"댓글 삭제 완료"}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"message":"삭제 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"message":"로그인이 필요한 요청입니다."}, status=status.HTTP_401_UNAUTHORIZED)