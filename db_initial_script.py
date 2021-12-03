# -*- coding: cp949 -*-

from custom_users.models import User
from members.models import Member, Registration
from lessons.models import Lesson, Attendance

# python manage.py shell < db_initial_script.py

# ������ ����
user = User.objects.create_superuser('������', password='000000')
user.is_admin=True
user.is_active=True
user.user_grade = 1
user.gender = 'm'
user.date_of_birth = '1990-01-06'
user.phone_number = '01031521438'
user.save()

user = User.objects.create_superuser('���ξ�', password='000000')
user.is_admin=True
user.is_active=True
user.user_grade = 3
user.gender = 'f'
user.date_of_birth = '1989-02-20'
user.phone_number = '01042003190'
user.save()

# ȸ�� ����
member = Member(name='������', gender='f', phone_number='01011112222')
member.save()

member = Member(name='������', gender='f', phone_number='01011112222')
member.save()

# ���� ����
lesson = Lesson(
    lesson_date='2021-12-03',
    lesson_time='19:30:00',
    teacher_id=User.objects.get(name='���ξ�')
)
lesson.save()

# ���� ����
attendance = Attendance(
    lesson_id=Lesson.objects.get(
        lesson_date='2021-12-03',
        lesson_time='19:30:00',
        teacher_id=User.objects.get(name='���ξ�')
    ),
    member_id=Member.objects.get(name='������'),
)
attendance.save()

attendance = Attendance(
    lesson_id=Lesson.objects.get(
        lesson_date='2021-12-03',
        lesson_time='19:30:00',
        teacher_id=User.objects.get(name='���ξ�')
    ),
    member_id=Member.objects.get(name='������'),
)
attendance.save()