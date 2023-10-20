from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):

    """ 사용자 모델을 생성하고 관리하는 클래스입니다. """

    def create_user(self, email, nickname, password):
        """ 일반 사용자를 생성하는 메서드입니다. """
        if not email:
            raise ValueError('유효하지 않은 이메일 형식입니다.')
        
        user = self.model(
            email=self.normalize_email(email),
            password=password,
            nickname=nickname,
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, nickname, password=None):
        """ 관리자를 생성하는 메서드입니다. """
        if not email:
            raise ValueError('유효하지 않은 이메일 형식입니다.')
        
        user = self.create_user(
            email,
            password=password,
            nickname=nickname,
        )

        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser) :
    """
    사용자 모델을 정의하는 클래스입니다.

    - email(필수) : 로그인 시 사용할 사용자의 이메일 주소입니다.
        - 다른 사용자의 이메일과 중복되지 않도록 설정합니다. (Unique)
    - password(필수) : 사용자의 비밀번호입니다.
    - nickname(필수) : 사용자의 활동 아이디입니다.
        - 다른 사용자의 닉네임과 중복되지 않도록 설정합니다. (Unique)
    - intro : 사용자의 소개글입니다.
    - profile_img : 사용자의 프로필 이미지입니다.
    - subscribe : 사용자 간 구독(팔로우) 관계입니다.
    - is_admin : 관리자 권한 여부입니다.
        - True 혹은 False를 저장할 수 있으며, 기본값으로 False를 저장하도록 설정합니다.
    """

    email = models.EmailField('이메일', max_length=255, unique=True)
    password = models.CharField('비밀번호', max_length=255)
    nickname = models.CharField('활동 아이디', max_length=30, unique=True)
    intro = models.CharField('소개글', max_length=500, null=True, blank=True)
    profile_img = models.ImageField('프로필 이미지', upload_to='user/profile_img/%Y/%M/%D/')
    subscribe = models.ManyToManyField('self', verbose_name='구독', symmetrical=False, related_name='subscribers')
    is_admin = models.BooleanField('관리자 여부', default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname',]

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        db_table = 'user'




