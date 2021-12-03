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
member = Member(name='�質��',	gender='f',	phone_number='01089839767')
member.save()
member = Member(name='������',	gender='f',	phone_number='01074767512')
member.save()
member = Member(name='������',	gender='m',	phone_number='01052072025')
member.save()
member = Member(name='�迬��',	gender='f',	phone_number='01053760506')
member.save()
member = Member(name='��ȣ��',	gender='f',	phone_number='01068185770')
member.save()
member = Member(name='������',	gender='f',	phone_number='01033516853')
member.save()
member = Member(name='���ο�',	gender='m',	phone_number='01033497073')
member.save()
member = Member(name='�ȼ���',	gender='f',	phone_number='01075775889')
member.save()
member = Member(name='������',	gender='f',	phone_number='01095761819')
member.save()
member = Member(name='���ؼ�',	gender='m',	phone_number='01046173396')
member.save()
member = Member(name='������',	gender='m',	phone_number='01039992266')
member.save()
member = Member(name='�Ż���',	gender='m',	phone_number='01021082500')
member.save()
member = Member(name='������',	gender='f',	phone_number='01041116704')
member.save()
member = Member(name='������',	gender='f',	phone_number='01029356123')
member.save()
member = Member(name='����',	gender='m', phone_number='01053265409')
member.save()
member = Member(name='ȣ��',	gender='f', phone_number='01053265409')
member.save()
member = Member(name='������',	gender='f',	phone_number='01046777244')
member.save()
member = Member(name='���ξ�',	gender='f',	phone_number='01089140201')
member.save()
member = Member(name='������',	gender='f',	phone_number='01090109146')
member.save()
member = Member(name='������',	gender='f',	phone_number='01026303003')
member.save()
member = Member(name='������',	gender='f',	phone_number='01096952858')
member.save()
member = Member(name='������',	gender='f',	phone_number='01099921479')
member.save()
member = Member(name='������',	gender='f',	phone_number='01089215041')
member.save()
member = Member(name='������',	gender='f',	phone_number='01050242126')
member.save()
member = Member(name='������',	gender='f',	phone_number='01071265784')
member.save()
member = Member(name='������',	gender='m',	phone_number='01056567270')
member.save()
member = Member(name='ȫ����',	gender='f',	phone_number='01099244732')
member.save()
member = Member(name='���ٿ�',	gender='m',	phone_number='0109189316')
member.save()
member = Member(name='������',	gender='f',	phone_number='01085292817')
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