from rest_framework import serializers
from post.models import Image, Post
from user.serializers import UserSerializer


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = "__all__"

    def create(self, validated_data):
        image = Image.objects.create(**validated_data)
        return image
    
class PostCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['title', 'post_img']

    def create(self, validated_data):
        print(validated_data)
        print(validated_data['post_img'])
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
        image_url = post.post_img.image
        return str(image_url)
    
    def get_like(self, post):
        who_liked = post.like.all().order_by('-id')
        users_data = UserSerializer(who_liked, many=True).data
        user_nicknames = []
        for user in users_data :
            user_nicknames.append(user['nickname'])
            return user_nicknames
        return user_nicknames

    class Meta:
        model = Post
        fields = "__all__"