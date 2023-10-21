from django.db import models
from django.conf import settings

class Post(models.Model):
    """
    - author : 게시물 작성자입니다.
        - 로그인 한 사용자를 자동으로 지정합니다.
    - title : 게시물 제목입니다.
    - like : 게시물을 좋아요 한 사용자와의 관계입니다.
    - post_img : 게시물에 등록할 이미지입니다.
    - created_at : 게시물이 작성된 일자 및 시간입니다.
        - 게시물이 작성된 시간을 자동으로 저장하도록 설정합니다.
    """

    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='작성자', on_delete=models.SET_NULL, null=True, related_name='posts')
    title = models.CharField("게시글 제목", max_length=50)
    like = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='좋아요', related_name='likes')
    post_img = models.OneToOneField('post.Image', verbose_name='게시물 이미지', on_delete=models.CASCADE)
    created_at = models.DateTimeField("생성 시각", auto_now_add=True)

    def __str__(self):
        return str(self.title)
    
    class Meta:
        db_table = 'post'

class Image(models.Model):
    """
    - image : 변환된 이미지의 url입니다.
    - created_at : 변환된 이미지가 생성된 일자 및 시간입니다.
        - 변환된 이미지가 생성된 시간을 자동으로 저장하도록 설정합니다.
    """
    image = models.ImageField('변환 이미지', upload_to='post/converted_img/%Y/%m/%d')
    created_at = models.DateTimeField("생성 시각", auto_now_add=True)

    class Meta:
        db_table = 'image'

class Comment(models.Model):
    """
    - author : 댓글 작성자입니다.
    - post : 댓글이 작성된 게시물입니다.
        - DB에는 게시물의 pk값이 저장됩니다.
    - content : 댓글의 내용입니다.
    - created_at : 댓글이 작성된 일자 및 시간입니다.
        - 댓글이 작성된 시간을 자동으로 저장하도록 설정합니다.
    """
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='작성자', related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey('post.Post', verbose_name='게시글', related_name='comments', on_delete=models.CASCADE)
    content = models.TextField('댓글 내용')
    created_at = models.DateTimeField("생성 시각", auto_now_add=True)

    class Meta:
        db_table = 'comment'