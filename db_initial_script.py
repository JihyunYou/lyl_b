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
member = Member.objects.create(
    name='�質��',
    gender='f',
    phone_number='01089839767',
    teacher_id=user,
    tue_yn=True,
    tue_time='16:00'
)
registration = Registration.objects.create(
    member_id=member,
    times=10,
    reg_date='2021-11-01',
    tuition=500000
)

member = Member.objects.create(
    name='������',	gender='f',	phone_number='01074767512',
    teacher_id=user
)
registration = Registration.objects.create(
    member_id=member,
    times=10,
    reg_date='2021-11-01',
    tuition=500000
)

member = Member.objects.create(
    name='������',	gender='m',	phone_number='01052072025',
    teacher_id=user
)
registration = Registration.objects.create(
    member_id=member,
    times=10,
    reg_date='2021-11-01',
    tuition=500000
)

member = Member.objects.create(
    name='�迬��',	gender='f',	phone_number='01053760506',
    teacher_id=user
)
registration = Registration.objects.create(
    member_id=member,
    times=10,
    reg_date='2021-11-01',
    tuition=500000
)

member = Member.objects.create(
    name='��ȣ��',	gender='f',	phone_number='01068185770',
    teacher_id=user
)
registration = Registration.objects.create(
    member_id=member,
    times=10,
    reg_date='2021-11-01',
    tuition=500000
)

member = Member.objects.create(
    name='������',	gender='f',	phone_number='01033516853',
    teacher_id=user
)
registration = Registration.objects.create(
    member_id=member,
    times=10,
    reg_date='2021-11-01',
    tuition=500000
)

member = Member.objects.create(
    name='���ο�',	gender='m',	phone_number='01033497073',
    teacher_id=user
)
registration = Registration.objects.create(
    member_id=member,
    times=10,
    reg_date='2021-11-01',
    tuition=500000
)

member = Member.objects.create(
    name='�ȼ���',	gender='f',	phone_number='01075775889',
    teacher_id=user
)
registration = Registration.objects.create(
    member_id=member,
    times=10,
    reg_date='2021-11-01',
    tuition=500000
)

member = Member.objects.create(
    name='������',	gender='f',	phone_number='01095761819',
    teacher_id=user
)
registration = Registration.objects.create(
    member_id=member,
    times=10,
    reg_date='2021-11-01',
    tuition=500000
)

member = Member.objects.create(
    name='���ؼ�',	gender='m',	phone_number='01046173396',
    teacher_id=user
)
registration = Registration.objects.create(
    member_id=member,
    times=10,
    reg_date='2021-11-01',
    tuition=500000
)

member = Member.objects.create(
    name='������',	gender='m',	phone_number='01039992266',
    teacher_id=user
)
registration = Registration.objects.create(
    member_id=member,
    times=10,
    reg_date='2021-11-01',
    tuition=500000
)

member = Member.objects.create(
    name='�Ż���',	gender='m',	phone_number='01021082500',
    teacher_id=user
)
registration = Registration.objects.create(
    member_id=member,
    times=10,
    reg_date='2021-11-01',
    tuition=500000
)

member = Member.objects.create(
    name='������',	gender='f',	phone_number='01041116704',
    teacher_id=user
)
registration = Registration.objects.create(
    member_id=member,
    times=10,
    reg_date='2021-11-01',
    tuition=500000
)

member = Member.objects.create(
    name='������',	gender='f',	phone_number='01029356123',
    teacher_id=user
)
registration = Registration.objects.create(
    member_id=member,
    times=10,
    reg_date='2021-11-01',
    tuition=500000
)

member = Member.objects.create(
    name='����',	gender='m', phone_number='01053265409',
    teacher_id=user
)
registration = Registration.objects.create(
    member_id=member,
    times=10,
    reg_date='2021-11-01',
    tuition=500000
)

member = Member.objects.create(
    name='ȣ��',	gender='f', phone_number='01053265409',
    teacher_id=user
)
registration = Registration.objects.create(
    member_id=member,
    times=10,
    reg_date='2021-11-01',
    tuition=500000
)

member = Member.objects.create(
    name='������',	gender='f',	phone_number='01046777244',
    teacher_id=user
)
registration = Registration.objects.create(
    member_id=member,
    times=10,
    reg_date='2021-11-01',
    tuition=500000
)

member = Member.objects.create(
    name='���ξ�',	gender='f',	phone_number='01089140201',
    teacher_id=user
)
registration = Registration.objects.create(
    member_id=member,
    times=10,
    reg_date='2021-11-01',
    tuition=500000
)

member = Member.objects.create(
    name='������',	gender='f',	phone_number='01090109146',
    teacher_id=user
)
registration = Registration.objects.create(
    member_id=member,
    times=10,
    reg_date='2021-11-01',
    tuition=500000
)

member = Member.objects.create(
    name='������',	gender='f',	phone_number='01026303003',
    teacher_id=user
)
registration = Registration.objects.create(
    member_id=member,
    times=10,
    reg_date='2021-11-01',
    tuition=500000
)

member = Member.objects.create(
    name='������',	gender='f',	phone_number='01096952858',
    teacher_id=user
)
registration = Registration.objects.create(
    member_id=member,
    times=10,
    reg_date='2021-11-01',
    tuition=500000
)

member = Member.objects.create(
    name='������',	gender='f',	phone_number='01099921479',
    teacher_id=user
)
registration = Registration.objects.create(
    member_id=member,
    times=10,
    reg_date='2021-11-01',
    tuition=500000
)

member = Member.objects.create(
    name='������',	gender='f',	phone_number='01089215041',
    teacher_id=user
)
registration = Registration.objects.create(
    member_id=member,
    times=10,
    reg_date='2021-11-01',
    tuition=500000
)

member = Member.objects.create(
    name='������',	gender='f',	phone_number='01050242126',
    teacher_id=user
)
registration = Registration.objects.create(
    member_id=member,
    times=10,
    reg_date='2021-11-01',
    tuition=500000
)

member = Member.objects.create(
    name='������',	gender='f',	phone_number='01071265784',
    teacher_id=user
)
registration = Registration.objects.create(
    member_id=member,
    times=10,
    reg_date='2021-11-01',
    tuition=500000
)

member = Member.objects.create(
    name='������',	gender='m',	phone_number='01056567270',
    teacher_id=user
)
registration = Registration.objects.create(
    member_id=member,
    times=10,
    reg_date='2021-11-01',
    tuition=500000
)

member = Member.objects.create(
    name='ȫ����',	gender='f',	phone_number='01099244732',
    teacher_id=user
)
registration = Registration.objects.create(
    member_id=member,
    times=10,
    reg_date='2021-11-01',
    tuition=500000
)

member = Member.objects.create(
    name='���ٿ�',	gender='m',	phone_number='0109189316',
    teacher_id=user
)
registration = Registration.objects.create(
    member_id=member,
    times=10,
    reg_date='2021-11-01',
    tuition=500000
)

member = Member.objects.create(
    name='������',	gender='f',	phone_number='01085292817',
    teacher_id=user
)
registration = Registration.objects.create(
    member_id=member,
    times=10,
    reg_date='2021-11-01',
    tuition=500000
)



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