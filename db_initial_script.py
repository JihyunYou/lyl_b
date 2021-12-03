# -*- coding: cp949 -*-

from custom_users.models import User
from members.models import Member, Registration
from lessons.models import Lesson, Attendance

# python manage.py shell < db_initial_script.py

# 관리자 계정
user = User.objects.create_superuser('유지현', password='000000')
user.is_admin=True
user.is_active=True
user.user_grade = 1
user.gender = 'm'
user.date_of_birth = '1990-01-06'
user.phone_number = '01031521438'
user.save()

user = User.objects.create_superuser('빙민아', password='000000')
user.is_admin=True
user.is_active=True
user.user_grade = 3
user.gender = 'f'
user.date_of_birth = '1989-02-20'
user.phone_number = '01042003190'
user.save()

# 회원 생성
member = Member(name='김은애', gender='f', phone_number='01011112222')
member.save()

member = Member(name='이은주', gender='f', phone_number='01011112222')
member.save()

# 수업 생성
lesson = Lesson(
    lesson_date='2021-12-03',
    lesson_time='19:30:00',
    teacher_id=User.objects.get(name='빙민아')
)
lesson.save()

# 수강 생성
attendance = Attendance(
    lesson_id=Lesson.objects.get(
        lesson_date='2021-12-03',
        lesson_time='19:30:00',
        teacher_id=User.objects.get(name='빙민아')
    ),
    member_id=Member.objects.get(name='김은애'),
)
attendance.save()

attendance = Attendance(
    lesson_id=Lesson.objects.get(
        lesson_date='2021-12-03',
        lesson_time='19:30:00',
        teacher_id=User.objects.get(name='빙민아')
    ),
    member_id=Member.objects.get(name='이은주'),
)
attendance.save()