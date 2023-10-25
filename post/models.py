from django.db import models
from django.conf import settings


class Post(models.Model):
    """
    - author : 게시물 작성자입니다.
        - 로그인 한 사용자를 자동으로 지정합니다.
    - title : 게시물 제목입니다.
    - content : 분석 결과입니다.
    - like : 게시물을 좋아요 한 사용자와의 관계입니다.
    - post_img : 게시물에 등록할 이미지입니다.
    - created_at : 게시물이 작성된 일자 및 시간입니다.
        - 게시물이 작성된 시간을 자동으로 저장하도록 설정합니다.
    """

    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='작성자',
                               on_delete=models.CASCADE, related_name='posts')
    title = models.CharField("게시글 제목", max_length=50)
    content = models.ForeignKey(
        'post.ConvertResult', verbose_name='분석 결과', on_delete=models.CASCADE, related_name='post_contents')
    like = models.ManyToManyField(
        settings.AUTH_USER_MODEL, verbose_name='좋아요', related_name='likes')
    post_img = models.ForeignKey(
        'post.ConvertResult', verbose_name='작성자', on_delete=models.CASCADE, related_name='post_imgs')
    created_at = models.DateTimeField("생성 시각", auto_now_add=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        db_table = 'post'


def original_image_upload_path(instance, filename):
    return f'user/{instance.owner.id}/original_img/{filename}'


def converted_image_upload_path(instance, filename):
    return f'user/{instance.owner.id}/converted_img/{filename}'


class ConvertResult(models.Model):
    """
    - owner : 이미지 변환을 요청하는 사용자입니다.
    - original_image : 사용자가 변환 요청한 이미지입니다.
    - converted_image : 변환된 이미지입니다.
    - result : 표정 분석 결과입니다.
    - created_at : 변환된 이미지가 생성된 일자 및 시간입니다.
        - 변환된 이미지가 생성된 시간을 자동으로 저장하도록 설정합니다.
    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              verbose_name='작성자', on_delete=models.CASCADE)
    original_image = models.ImageField(
        '원본 이미지', upload_to=original_image_upload_path)
    converted_image = models.ImageField(
        '변환 이미지', upload_to=converted_image_upload_path, null=True, blank=True)
    result = models.TextField('분석 결과', null=True, blank=True)
    created_at = models.DateTimeField("생성 시각", auto_now_add=True)

    class Meta:
        db_table = 'convert_result'


class Comment(models.Model):
    """
    - author : 댓글 작성자입니다.
    - post : 댓글이 작성된 게시물입니다.
        - DB에는 게시물의 pk값이 저장됩니다.
    - content : 댓글의 내용입니다.
    - created_at : 댓글이 작성된 일자 및 시간입니다.
        - 댓글이 작성된 시간을 자동으로 저장하도록 설정합니다.
    """
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='작성자',
                               related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey('post.Post', verbose_name='게시글',
                             related_name='comments', on_delete=models.CASCADE)
    content = models.TextField('댓글 내용')
    created_at = models.DateTimeField("생성 시각", auto_now_add=True)

    class Meta:
        db_table = 'comment'
