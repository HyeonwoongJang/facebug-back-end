from rest_framework import serializers
from post.models import ConvertResult, Post, Comment
from user.serializers import UserSerializer


class ConvertSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConvertResult
        fields = ['id', 'original_image', 'converted_image', 'result']

    def create(self, validated_data):
        instance = ConvertResult.objects.create(**validated_data)
        return instance


class PostCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'post_img']

    def create(self, validated_data):
        # print(validated_data)
        # print(validated_data['post_img'])
        post = Post.objects.create(**validated_data)

        return post


class PostListSerializer(serializers.ModelSerializer):

    author_nickname = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    like = serializers.SerializerMethodField()

    def get_author_nickname(self, post):
        return post.author.nickname

    def get_likes_count(self, post):
        return post.like.count()

    def get_image_url(self, post):
        images = post.post_img
        image_url = images.converted_image
        return str(image_url)

    def get_like(self, post):
        who_liked = post.like.all().order_by('-id')
        # print(who_liked)
        users_data = UserSerializer(who_liked, many=True).data
        # print(users_data)
        user_info = []
        for user in users_data:
            user_info.append([user['id'], user['nickname']])
        return user_info

    class Meta:
        model = Post
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['content',]

    def create(self, validated_data):
        comment = Comment.objects.create(**validated_data)
        return comment


class CommentListSerializer(serializers.ModelSerializer):

    author_nickname = serializers.SerializerMethodField()

    def get_author_nickname(self, comment):
        return comment.author.nickname

    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'author_nickname', 'created_at']
