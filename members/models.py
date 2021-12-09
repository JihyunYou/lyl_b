from django.db import models
from django.core.validators import RegexValidator

# 유저(강사) 모델 import
from custom_users.models import User as Teacher


GENDER_CHOICES = [
    ('m', '남자'), ('f', '여자')
]

DAY_LESSON_YN = [
    (True, '수업 있음'), (False, '수업 없음')
]

REGISTRATION_TYPE = [
    (1, '첫등록'), (2, '재등록')
]

# 강습 회원
class Member(models.Model):
    name = models.CharField(
        # help_text="회원 이름",
        max_length=20, null=False)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1, null=False)
    date_of_birth = models.DateField(null=True)

    phoneNumberRegex = RegexValidator(regex=r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$')
    phone_number = models.CharField(validators=[phoneNumberRegex], max_length=11)

    teacher_id = models.ForeignKey(
        Teacher, related_name="member_teacher", on_delete=models.SET_NULL, db_column="teacher_id",
        null=True
    )

    mon_yn = models.BooleanField(choices=DAY_LESSON_YN, default=False)
    mon_time = models.TimeField(null=True, blank=True)
    tue_yn = models.BooleanField(choices=DAY_LESSON_YN, default=False)
    tue_time = models.TimeField(null=True, blank=True)
    wed_yn = models.BooleanField(choices=DAY_LESSON_YN, default=False)
    wed_time = models.TimeField(null=True, blank=True)
    thu_yn = models.BooleanField(choices=DAY_LESSON_YN, default=False)
    thu_time = models.TimeField(null=True, blank=True)
    fri_yn = models.BooleanField(choices=DAY_LESSON_YN, default=False)
    fri_time = models.TimeField(null=True, blank=True)
    sat_yn = models.BooleanField(choices=DAY_LESSON_YN, default=False)
    sat_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return  self.name

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
    reg_date = models.DateField(null=True)
    tuition = models.IntegerField(null=False)

    input_dtime = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['reg_date']

    def __str__(self):
        """String for representing the Model object."""
        # return Member(primary_key=self.member_id).name
        return self.member_id.name
