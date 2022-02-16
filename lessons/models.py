from django.db import models

from django.core.validators import MaxValueValidator, MinValueValidator

# 유저(강사), 회원 모델 import
from custom_users.models import User as Teacher
from members.models import Member


GENDER_CHOICES = [
    ('s', '개인'), ('p', '듀엣')
]

ATTENDANCE_STATUS = [
    (0, '수업 예정'),
    (1, '수업 완료'),
    (2, '사전 취소'),
    (3, '당일 취소'),
    (4, '홀딩'),
]


class History(models.Model):
    lesson_date = models.DateField(null=False)
    lesson_time = models.TimeField(null=False)

    created_by = models.ForeignKey(
        Teacher, on_delete=models.SET_NULL, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)


# 수업 관리
class Lesson(models.Model):
    lesson_date = models.DateField(null=False)
    lesson_time = models.TimeField(null=False)

    teacher_id = models.ForeignKey(
        Teacher, related_name="lesson_teacher", on_delete=models.SET_NULL, db_column="teacher_id",
        null=True
    )

    lesson_type = models.CharField(choices=GENDER_CHOICES, max_length=1, null=False)
    input_dtime = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['lesson_date', 'lesson_time', 'teacher_id'],
                name='unique_lesson',
            )
        ]
        ordering = ['-lesson_date']


# 출석 관리
class Attendance(models.Model):
    lesson_id = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        db_column="lesson_id",
        null=False
    )
    member_id = models.ForeignKey(
        Member, related_name="attendance_member", on_delete=models.CASCADE, db_column="member_id",
        null=False
    )

    # 출석 상태
    #   0: 수업 예정
    #   1: 정상 출석
    #   2: 사전 취소
    #   3: 당일 취소
    #   4: 회원권 홀딩
    status = models.IntegerField(
        choices=ATTENDANCE_STATUS,
        null=True, blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(3)
        ],
        default=0
    )

    input_dtime = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['lesson_id', 'member_id'],
                name='unique_lesson_attendance',
            )
        ]
        ordering = ['lesson_id']