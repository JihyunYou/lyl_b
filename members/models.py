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

# 강습 회원
class Member(models.Model):
    id = models.BigAutoField(help_text="Post ID", primary_key=True)
    name = models.CharField(max_length=20, null=False)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1, null=False)
    date_of_birth = models.DateField(null=True)

    phoneNumberRegex = RegexValidator(regex=r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$')
    phone_number = models.CharField(validators=[phoneNumberRegex], max_length=11)

    teacher_id = models.ForeignKey(
        Teacher, related_name="member_teacher", on_delete=models.SET_NULL, db_column="teacher_id",
        null=True
    )


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

    def __str__(self):
        """String for representing the Model object."""
        # return Member(primary_key=self.member_id).name
        return self.member_id.name
