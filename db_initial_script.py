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
member = Member(name='김나영',	gender='f',	phone_number='01089839767')
member.save()
member = Member(name='박지은',	gender='f',	phone_number='01074767512')
member.save()
member = Member(name='성기훈',	gender='m',	phone_number='01052072025')
member.save()
member = Member(name='김연경',	gender='f',	phone_number='01053760506')
member.save()
member = Member(name='임호연',	gender='f',	phone_number='01068185770')
member.save()
member = Member(name='성민주',	gender='f',	phone_number='01033516853')
member.save()
member = Member(name='이인용',	gender='m',	phone_number='01033497073')
member.save()
member = Member(name='안서현',	gender='f',	phone_number='01075775889')
member.save()
member = Member(name='오수정',	gender='f',	phone_number='01095761819')
member.save()
member = Member(name='최준석',	gender='m',	phone_number='01046173396')
member.save()
member = Member(name='강정금',	gender='m',	phone_number='01039992266')
member.save()
member = Member(name='신상일',	gender='m',	phone_number='01021082500')
member.save()
member = Member(name='김은상',	gender='f',	phone_number='01041116704')
member.save()
member = Member(name='곽도현',	gender='f',	phone_number='01029356123')
member.save()
member = Member(name='현주',	gender='m', phone_number='01053265409')
member.save()
member = Member(name='호영',	gender='f', phone_number='01053265409')
member.save()
member = Member(name='윤정수',	gender='f',	phone_number='01046777244')
member.save()
member = Member(name='윤민아',	gender='f',	phone_number='01089140201')
member.save()
member = Member(name='강민희',	gender='f',	phone_number='01090109146')
member.save()
member = Member(name='김은애',	gender='f',	phone_number='01026303003')
member.save()
member = Member(name='김은주',	gender='f',	phone_number='01096952858')
member.save()
member = Member(name='임지은',	gender='f',	phone_number='01099921479')
member.save()
member = Member(name='박정순',	gender='f',	phone_number='01089215041')
member.save()
member = Member(name='윤진희',	gender='f',	phone_number='01050242126')
member.save()
member = Member(name='차정윤',	gender='f',	phone_number='01071265784')
member.save()
member = Member(name='이준휘',	gender='m',	phone_number='01056567270')
member.save()
member = Member(name='홍서연',	gender='f',	phone_number='01099244732')
member.save()
member = Member(name='윤다영',	gender='m',	phone_number='0109189316')
member.save()
member = Member(name='민은주',	gender='f',	phone_number='01085292817')
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
    member_id=Member.objects.get(name='임지은'),
)
attendance.save()