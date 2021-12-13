import datetime

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.forms import ModelForm, inlineformset_factory
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView

import lessons
from custom_users.models import User
from .models import Lesson, Attendance, Member


class LessonForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(LessonForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'

    class Meta:
        model = Lesson
        fields = '__all__'
        labels = {
            'lesson_date': '수업 날짜',
            'lesson_time': '수업 시간',
            'teacher_id': '담당 강사',
            'lesson_type': '수업 종류'
        }
        # widgets = {
        #     'lesson_time': forms.TimeInput(format="%H:%M"),
        # }


class AttendanceForm(ModelForm):
    class Meta:
        model = Attendance
        fields = ['member_id']


LessonAttendanceFormset = inlineformset_factory(
    Lesson,
    Attendance,
    form=AttendanceForm,
    max_num=2,
    min_num=1,
    validate_min=True,
    extra=2,
    labels={
        'member_id': '회원명'
    }
)


class LessonCreate(CreateView):
    model = Lesson
    fields = [
        'lesson_date', 'lesson_time', 'teacher_id', 'lesson_type',
    ]

    def form_valid(self, form):
        return super(LessonCreate, self).form_valid(form)

    # return redirect(detail, lesson_id=model.id)


def get_all_events():
    event_arr = []

    lesson_objects = Lesson.objects.all()
    for i in lesson_objects:
        event_sub_arr = {}
        attendance_objects = Attendance.objects.filter(lesson_id=i.id).select_related("member_id")
        # title
        #   수강 회원명, 수업 상태
        str_title = ''
        for j, val in enumerate(attendance_objects):
            if j != 0:
                str_title += ', '
            str_title += str(val.member_id.name)
        str_title += ' [' + val.get_status_display() + ']'
        event_sub_arr['title'] = str_title

        # Event Color 설정
        #   수업예정: #198754
        #   수업완료: #0d6dfd
        #   사전취소: #ffc107
        #   당일취소: #dc3546
        color_array =['#198754', '#0d6dfd', '#ffc107', '#dc3546']
        event_sub_arr['color'] = color_array[val.status]

        # start, end
        start_dt = datetime.datetime.strptime(
            str(i.lesson_date) + ' ' + str(i.lesson_time),
            "%Y-%m-%d %H:%M:%S"
        ).strftime("%Y-%m-%d %H:%M:%S")

        end_dt = datetime.datetime.strptime(
            str(i.lesson_date) + ' ' + str(cal_end_time(i.lesson_time)),
            "%Y-%m-%d %H:%M:%S"
        ).strftime("%Y-%m-%d %H:%M:%S")

        event_sub_arr['start'] = start_dt
        event_sub_arr['end'] = end_dt

        event_sub_arr['lesson_id'] = i.id

        event_arr.append(event_sub_arr)

    return event_arr


#   라일비 프로젝트 메인 페이지, 월 스케쥴
def index(request):
    # Form
    lesson_form = LessonForm
    attendance_formset = LessonAttendanceFormset

    # Context
    context = {}

    # 일정 생성
    # if request.POST:
    #     lesson_form = LessonForm(request.POST)
    #
    #     if lesson_form.is_valid():
    #         lesson = lesson_form.save(commit=False)
    #
    #         # 스케쥴 시간 체크
    #         #  수업일에 수업시간 사이에 겹치는 수업이 있는지 체크
    #         if check_lesson_schedule(lesson):   # 이상 없는 경우
    #             attendance_formset = LessonAttendanceFormset(request.POST, instance=lesson)
    #             if attendance_formset.is_valid():
    #                 lesson.save()
    #                 attendance_formset.save()
    #                 # 정상 저장한 경우, 새로고침시 POST 가 다시 작동되지 않도록 하기 위해
    #                 # reverse 를 사용하여 동일한 view 로 redirection
    #                 return HttpResponseRedirect(reverse(lessons.views.index))
    #         else:
    #             context['error'] = "이미 수업 스케쥴이 있는 시간입니다!"

    context['lesson_form'] = lesson_form
    context['attendance_formset'] = attendance_formset
    context['events'] = get_all_events

    return render(
        request,
        'lessons/index.html',
        context
    )


# Lesson List 페이지
def list(request):
    lesson_objects = Lesson.objects.all()

    return render(
        request,
        'lessons/lesson_list.html',
        {
            'lesson_objects': lesson_objects,
        }
    )


# Lesson 상세 페이지, 출석 관리
def detail(request, lesson_id):
    try:
        lesson_object = Lesson.objects.get(id=lesson_id)
        attendance_objects = Attendance.objects.filter(lesson_id=lesson_id)

        # 수업 정보 수정
        form = LessonForm(request.POST or None, instance=lesson_object)
        print("test")
        if form.is_valid():
            form.save()
            return redirect(detail, lesson_id=lesson_id)

    except:
        raise Http404("존재하지 않는 수업입니다.")
    return render(
        request,
        'lessons/lesson_detail.html',
        {
            'lesson_object': lesson_object,
            'attendance_objects': attendance_objects,
            'form': form,
        }
    )


# 기본 스케쥴 생성
def create_default_schedule(request):
    # 로그인 하지 않은 사용자가 URL을 통해 회원을 삭제하는 것을 막음
    if not request.user.is_authenticated:
        print("권한 없는 사용자의 일정 등록 차단")
        return redirect('/')

    member_objects = Member.objects.filter(status=1)

    if request.POST:
        input_date = request.POST.get('schedule_date')
        input_date = datetime.datetime.strptime(input_date, '%Y-%m-%d').date()

        start_date = input_date + datetime.timedelta(days=-1 * input_date.weekday())
        end_date = start_date + datetime.timedelta(days=5)
        print("시작일: " + str(start_date))
        print("종료일: " + str(end_date))

        for member in member_objects:
            try:
                if member.mon_yn:
                    # 수업 생성, 이미 수업 일정이 있다면 Get
                    lesson, created = Lesson.objects.get_or_create(
                        lesson_date=start_date,
                        lesson_time=member.mon_time,
                        teacher_id=User.objects.get(pk=member.teacher_id.id)
                    )

                    # 수강 생성, 이미 등록 정보가 있다면 생성하지 않는다.
                    attendance, created = Attendance.objects.get_or_create(
                        lesson_id=lesson,
                        member_id=member,
                    )
                if member.tue_yn:
                    # 수업 생성, 이미 수업 일정이 있다면 Get
                    lesson, created = Lesson.objects.get_or_create(
                        lesson_date=start_date + datetime.timedelta(days=1),
                        lesson_time=member.tue_time,
                        teacher_id=User.objects.get(pk=member.teacher_id.id)
                    )

                    # 수강 생성, 이미 등록 정보가 있다면 생성하지 않는다.
                    attendance, created = Attendance.objects.get_or_create(
                        lesson_id=lesson,
                        member_id=member,
                    )
                if member.wed_yn:
                    # 수업 생성, 이미 수업 일정이 있다면 Get
                    lesson, created = Lesson.objects.get_or_create(
                        lesson_date=start_date + datetime.timedelta(days=2),
                        lesson_time=member.wed_time,
                        teacher_id=User.objects.get(pk=member.teacher_id.id)
                    )

                    # 수강 생성, 이미 등록 정보가 있다면 생성하지 않는다.
                    attendance, created = Attendance.objects.get_or_create(
                        lesson_id=lesson,
                        member_id=member,
                    )
                if member.thu_yn:
                    # 수업 생성, 이미 수업 일정이 있다면 Get
                    lesson, created = Lesson.objects.get_or_create(
                        lesson_date=start_date + datetime.timedelta(days=3),
                        lesson_time=member.thu_time,
                        teacher_id=User.objects.get(pk=member.teacher_id.id)
                    )

                    # 수강 생성, 이미 등록 정보가 있다면 생성하지 않는다.
                    attendance, created = Attendance.objects.get_or_create(
                        lesson_id=lesson,
                        member_id=member,
                    )
                if member.fri_yn:
                    # 수업 생성, 이미 수업 일정이 있다면 Get
                    lesson, created = Lesson.objects.get_or_create(
                        lesson_date=start_date + datetime.timedelta(days=4),
                        lesson_time=member.fri_time,
                        teacher_id=User.objects.get(pk=member.teacher_id.id)
                    )

                    # 수강 생성, 이미 등록 정보가 있다면 생성하지 않는다.
                    attendance, created = Attendance.objects.get_or_create(
                        lesson_id=lesson,
                        member_id=member,
                    )
                if member.sat_yn:
                    # 수업 생성, 이미 수업 일정이 있다면 Get
                    lesson, created = Lesson.objects.get_or_create(
                        lesson_date=start_date + datetime.timedelta(days=5),
                        lesson_time=member.sat_time,
                        teacher_id=User.objects.get(pk=member.teacher_id.id)
                    )

                    # 수강 생성, 이미 등록 정보가 있다면 생성하지 않는다.
                    attendance, created = Attendance.objects.get_or_create(
                        lesson_id=lesson,
                        member_id=member,
                    )

            except:
                return HttpResponse("error")
                # lesson_form = LessonForm
                # attendance_formset = LessonAttendanceFormset
                # context = {'lesson_form': lesson_form, 'attendance_formset': attendance_formset}

    return redirect('/')


def create_manual_schedule(request):
    print('강습 일정 수동 등록')

    # 로그인 하지 않은 사용자가 URL을 통해 회원을 삭제하는 것을 막음
    if not request.user.is_authenticated:
        print("권한 없는 사용자의 일정 등록 차단")
        return redirect('/')

    print('유저 네임: "' + request.user.name)

    lesson_form = LessonForm
    attendance_formset = LessonAttendanceFormset
    context = {'lesson_form': lesson_form, 'attendance_formset': attendance_formset}

    if request.POST:
        lesson_form = LessonForm(request.POST)
        if lesson_form.is_valid():
            lesson = lesson_form.save(commit=False)

            # 스케쥴 시간 체크
            #  수업일에 수업시간 사이에 겹치는 수업이 있는지 체크
            if not check_lesson_schedule(lesson):
                context['error'] = "이미 수업 스케쥴이 있는 시간입니다!"
                return render(
                    request,
                    'lessons/lesson_create.html',
                    context
                )

            lesson.save()
            attendance_formset = LessonAttendanceFormset(request.POST, instance=lesson)
            if attendance_formset.is_valid():
                attendance_formset.save()
            return redirect('/')

    return render(
        request,
        'lessons/lesson_create.html',
        {
            'lesson_form': lesson_form,
            'attendance_formset': attendance_formset,
        }
    )


# 출석관리
def manage_attendance(request):
    # 로그인 하지 않은 사용자가 URL을 통해 회원을 삭제하는 것을 막음
    if not request.user.is_authenticated:
        print("권한 없는 사용자")
        return redirect('/')

    print("test")
    lesson_id = request.POST['lesson_id']
    member_id = request.POST['member_id']
    attendance_flag = request.POST['attendance_flag']
    attendance_object = Attendance.objects.get(lesson_id=lesson_id, member_id=member_id)
    attendance_object.status = attendance_flag
    attendance_object.save()

    # 원래 페이지로 보내기 위한 변수
    next = request.POST.get('next', '/')

    return HttpResponseRedirect(next)


# 수업의 경우 Foreign 키 제약사항으로 출석정보가 함께 삭제 됨
def delete_lesson(request, lesson_id):
    try:
        lesson_object = Lesson.objects.get(pk=lesson_id)
        # registration_objects = Registration.objects.filter(member_id=member_id)
        # registration_objects.delete()
        lesson_object.delete()
    except:
        raise Http404("존재하지 않는 수업 일정입니다.")

    return redirect('/')


# 겹치는 수업 시간 체크
def check_lesson_schedule(lesson):
    ex_lesson_objects = Lesson.objects.filter(
        teacher_id=lesson.teacher_id,
        lesson_date=lesson.lesson_date,
    )

    result = True

    for ex_lesson in ex_lesson_objects:
        if ex_lesson.lesson_time <= lesson.lesson_time <= cal_end_time(ex_lesson.lesson_time):
            result = False

        if ex_lesson.lesson_time <= cal_end_time(lesson.lesson_time) <= cal_end_time(ex_lesson.lesson_time):
            result = False

    return result


# 시간 계산은 dummy 일자를 붙여 계산한 후 시간 추출하는 방식 사용
def cal_end_time(start_time):
    end_time = datetime.datetime(100, 1, 1, start_time.hour, start_time.minute, start_time.second)
    end_time = end_time + datetime.timedelta(minutes=50)
    return end_time.time()
