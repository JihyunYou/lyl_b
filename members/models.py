from django.db import models
from django.core.validators import RegexValidator

# 유저(강사) 모델 import
from custom_users.models import User as Teacher


GENDER_CHOICES = [
    ('m', '남자'), ('f', '여자')
]

REGISTRATION_TYPE = [
    (1, '첫등록'), (2, '재등록')
]

MEMBER_STATUS = [
    (1, '진행중'), (2, '일시중지'), (3, '만료')
]

DAY_OF_WEEK = [
    (1, '월요일'), (2, '화요일'), (3, '수요일'), (4, '목요일'), (5, '금요일'), (6, '토요일'), (7, '일요일'),
]

METHOD_OF_PAYMENT = [
    (1, '현금(계좌이체)'), (2, '현금(현물)'), (3, '카드')
]

# 강습 회원
class Member(models.Model):
    objects = None
    name = models.CharField(
        # help_text="회원 이름",
        max_length=20, null=False)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1, null=False)
    date_of_birth = models.DateField(null=True)

    phoneNumberRegex = RegexValidator(regex=r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$')
    phone_number = models.CharField(
        validators=[phoneNumberRegex],
        max_length=11,
        null=True,
    )

    teacher_id = models.ForeignKey(
        Teacher, related_name="member_teacher", on_delete=models.SET_NULL, db_column="teacher_id",
        null=True
    )

    status = models.IntegerField(choices=MEMBER_STATUS, default=1)

    class Meta:
        ordering = ['status', 'name',]

    def __str__(self):
        return self.name


class DefaultSchedule(models.Model):
    member_id = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        db_column='member_id',
        null=False
    )
    day_of_week = models.IntegerField(
        choices=DAY_OF_WEEK,
        null=True
    )
    lesson_time = models.TimeField(
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['member_id', 'day_of_week', 'lesson_time'],
                name='unique_default_schedule'
            )
        ]
        ordering = ['member_id', 'day_of_week']


# 등록 관리
class Registration(models.Model):
    # Django 는 Composite PK 를 지원하지 않음
    member_id = models.ForeignKey(
        Member, related_name="registration_member", on_delete=models.PROTECT, db_column="member_id"
    )
    # 첫등록: 1, 재등록: 2 이상
    reg_seq = models.IntegerField(null=True)

    # 등록횟수
    times = models.IntegerField(null=False)

    # 등록일
    reg_date = models.DateField(null=True)

    # 수업료
    tuition = models.IntegerField(null=False)

    # 결제수단
    payment = models.IntegerField(
        choices=METHOD_OF_PAYMENT,
        null=True
    )

    description = models.TextField(
        null=True
    )

    input_dtime = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['reg_date', 'member_id']

    def __str__(self):
        """String for representing the Model object."""
        # return Member(primary_key=self.member_id).name
        return self.member_id.name
