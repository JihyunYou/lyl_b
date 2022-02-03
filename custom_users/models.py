from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator

# 유저 종류 설정
GRADE_IN_ROLE_CHOICES = [
    (1, '관리자'), (2, '대표'), (3, '강사'), (4, '강습회원')
]

GENDER_CHOICES = [
    ('m', '남자'), ('f', '여자')
]


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, name, password=None):
        # if not email:
        #     raise ValueError('Users must have an email address')

        user = self.model(
            # email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, password):
        user = self.create_user(
            # email,
            name=name,
            password=password,
        )
        # user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    # Custom 헬퍼 클래스를 사용하도록 설정
    objects = UserManager()

    # email = models.EmailField(
    #     verbose_name='email',
    #     max_length=255,
    #     unique=True,
    # )

    # 이름 - ID 역할
    name = models.CharField(
        verbose_name='name',
        max_length=20, unique=True, null=False)
    USERNAME_FIELD = 'name'  # Username을 name로 명시

    # 사이트 사용자 종류
    #   1: 사이트 관리자
    #   2: 업체 대표
    #   3: 강사
    #   4: 강습회원
    user_grade = models.IntegerField(
        choices=GRADE_IN_ROLE_CHOICES,
        null=True, blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(4)
        ],
        default=4
    )

    gender = models.CharField(choices=GENDER_CHOICES, max_length=1, null=False)

    date_of_birth = models.DateField(null=True)

    phoneNumberRegex = RegexValidator(regex=r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$')
    phone_number = models.CharField(validators=[phoneNumberRegex], max_length=11)

    # is_staff: admin site 접근 가능 여부
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    # is_superuser = models.BooleanField(default=False)
    # is_staff = models.BooleanField(default=False)

    # REQUIRED_FIELDS 안 쓰면 createsuperuser 할 때 안 나타남
    # REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

    # 커스텀 유저 모델을 기본 유저 모델로 사용하기 위해 구현한 부분
    #   True를 반환하여 권한이 있음을 알림
    def has_perm(self, perm, obj=None):
        return True

    #   True를 반환하여 주어진 App의 모델에 접근 가능하도록 함
    def has_module_perms(self, app_label):
        return True

    #   True 가 반환되면 관리자 화면에 로그인 가능
    @property
    def is_staff(self):
        return self.is_admin
