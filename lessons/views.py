import datetime

from crispy_forms.helper import FormHelper
from django import forms
from django.forms import ModelForm, inlineformset_factory
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView

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


#   라일비 프로젝트 메인 페이지, 월 스케쥴
def index(request):
    lesson_objects = Lesson.objects.all()

    event_arr = []
    # if request.Get:
    #     event_arr = []
    # if request.GET.get('event_type') == "all":
    #     all_events = Events.objects.all()
    # else:
    #     all_events = Events.objects.filter(event_type__icontains=request.GET.get('event_type'))

    for i in lesson_objects:
        event_sub_arr = {}
        attendance_objects = Attendance.objects.filter(lesson_id=i.id).select_related("member_id")
        # title
        str_title = ''
        for j, val in enumerate(attendance_objects):
            if j != 0:
                str_title += ', '
            str_title += str(val.member_id.name)
        event_sub_arr['title'] = str_title

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

    return render(
        request,
        'lessons/index.html',
        {
            'lesson_objects': lesson_objects,
            'events': event_arr
        }
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
    member_objects = Member.objects.all()

    if request.POST:
        input_date = request.POST.get('schedule_date')
        input_date = datetime.datetime.strptime(input_date, '%Y-%m-%d').date()

        start_date = input_date + datetime.timedelta(days=-1*input_date.weekday())
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
                elif member.tue_yn:
                    # 수업 생성, 이미 수업 일정이 있다면 Get
                    lesson, created = Lesson.objects.get_or_create(
                        lesson_date=start_date,
                        lesson_time=member.tue_time,
                        teacher_id=User.objects.get(pk=member.teacher_id.id)
                    )

                    # 수강 생성, 이미 등록 정보가 있다면 생성하지 않는다.
                    attendance, created = Attendance.objects.get_or_create(
                        lesson_id=lesson,
                        member_id=member,
                    )
                elif member.wed_yn:
                    # 수업 생성, 이미 수업 일정이 있다면 Get
                    lesson, created = Lesson.objects.get_or_create(
                        lesson_date=start_date,
                        lesson_time=member.wed_time,
                        teacher_id=User.objects.get(pk=member.teacher_id.id)
                    )

                    # 수강 생성, 이미 등록 정보가 있다면 생성하지 않는다.
                    attendance, created = Attendance.objects.get_or_create(
                        lesson_id=lesson,
                        member_id=member,
                    )
                elif member.thu_yn:
                    # 수업 생성, 이미 수업 일정이 있다면 Get
                    lesson, created = Lesson.objects.get_or_create(
                        lesson_date=start_date,
                        lesson_time=member.thu_time,
                        teacher_id=User.objects.get(pk=member.teacher_id.id)
                    )

                    # 수강 생성, 이미 등록 정보가 있다면 생성하지 않는다.
                    attendance, created = Attendance.objects.get_or_create(
                        lesson_id=lesson,
                        member_id=member,
                    )
                elif member.fri_yn:
                    # 수업 생성, 이미 수업 일정이 있다면 Get
                    lesson, created = Lesson.objects.get_or_create(
                        lesson_date=start_date,
                        lesson_time=member.fri_time,
                        teacher_id=User.objects.get(pk=member.teacher_id.id)
                    )

                    # 수강 생성, 이미 등록 정보가 있다면 생성하지 않는다.
                    attendance, created = Attendance.objects.get_or_create(
                        lesson_id=lesson,
                        member_id=member,
                    )
                elif member.sat_yn:
                    # 수업 생성, 이미 수업 일정이 있다면 Get
                    lesson, created = Lesson.objects.get_or_create(
                        lesson_date=start_date,
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

    return redirect('/lesson/')


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
