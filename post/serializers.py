from rest_framework import serializers
from post.models import Image, Post


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
