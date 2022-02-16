import datetime

from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput
from crispy_forms.helper import FormHelper
from django.forms import ModelForm, inlineformset_factory
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView

from custom_users.models import User
from members.models import DefaultSchedule
from .models import Lesson, Attendance, Member, History


class LessonForm(ModelForm):
    class Meta:
        model = Lesson
        fields = '__all__'
        labels = {
            'lesson_date': '수업 날짜',
            'lesson_time': '수업 시간',
            'teacher_id': '담당 강사',
            'lesson_type': '수업 종류'
        }
        widgets = {
            'lesson_date': DatePickerInput(
                options={
                    'format': 'YYYY-MM-DD',
                    'locale': 'ko',
                }
            ),
            'lesson_time': TimePickerInput(
                options={
                    'stepping': 10,
                }
            ),
        }
    def __init__(self, *args, **kwargs):
        super(LessonForm, self).__init__(*args, **kwargs)
        self.fields['teacher_id'].queryset = User.objects.filter(user_grade=3)


class AttendanceForm(ModelForm):
    class Meta:
        model = Attendance
        fields = ['member_id']

    def __init__(self, *args, **kwargs):
        super(AttendanceForm, self).__init__(*args, **kwargs)
        self.fields['member_id'].queryset = Member.objects.filter(status=1)


LessonAttendanceFormset = inlineformset_factory(
    Lesson,
    Attendance,
    form=AttendanceForm,
    max_num=2,
    min_num=1,
    validate_min=True,
    extra=2,
    labels={
        'member_id': '회원'
    }
)


class AttendanceManagementForm(ModelForm):
    class Meta:
        model = Attendance
        fields = ['status']
        labels = {
            'status': '출석 상태'
        }


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
        # 2022.01.23 빙민아 요청 사항 처리
        #   - 듀엣인데 한명마 등록시 공석 출력
        if i.lesson_type == 'p' and j == 0:
            str_title += ", 공석"
        str_title += ' [' + val.get_status_display() + ']'
        event_sub_arr['title'] = str_title

        # Event Color 설정
        #   수업예정: #198754
        #   수업완료: #0d6dfd
        #   사전취소: #ffc107
        #   당일취소: #dc3546
        #   홀   딩: #0dcaf0
        color_array =['#198754', '#0d6dfd', '#ffc107', '#dc3546', '#0dcaf0']
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
    context = {}

    try:
        lesson_object = Lesson.objects.get(id=lesson_id)
        attendance_objects = Attendance.objects.filter(lesson_id=lesson_id)

        # 수업 정보 수정
        form = LessonForm(request.POST or None, instance=lesson_object)

        # 출석 정보 수정 Form
        attendance_form = AttendanceManagementForm

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
            'attendance_form': attendance_form,
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
                default_schedule_objects = DefaultSchedule.objects.filter(member_id=member)
                for default_schedule in default_schedule_objects:
                    print(default_schedule.member_id)
                    print(default_schedule.day_of_week)
                    print(default_schedule.lesson_time)
                    # 수업 생성, 이미 수업 일정이 있다면 Get
                    lesson, created = Lesson.objects.get_or_create(
                        lesson_date=start_date + datetime.timedelta(days=default_schedule.day_of_week - 1),
                        lesson_time=default_schedule.lesson_time,
                        teacher_id=User.objects.get(pk=member.teacher_id.id)
                    )

                    # 수강 생성, 이미 등록 정보가 있다면 생성하지 않는다.
                    attendance, created = Attendance.objects.get_or_create(
                        lesson_id=lesson,
                        member_id=member,
                    )

            except Exception as e:
                print(e)
                return HttpResponse("error")

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
def manage_attendance(request, lesson_id):
    # 로그인 하지 않은 사용자가 URL을 통해 회원을 삭제하는 것을 막음
    if not request.user.is_authenticated:
        print("권한 없는 사용자")
        return redirect('/')

    member_id = request.POST['member_id']
    status = request.POST['status']

    attendance_object = Attendance.objects.get(lesson_id=lesson_id, member_id=member_id)
    attendance_object.status = status
    attendance_object.save()

    # 원래 페이지로 보내기 위한 변수
    # next = request.POST.get('next', '/')

    return redirect(detail, lesson_id)


# 수업의 경우 Foreign 키 제약사항으로 출석정보가 함께 삭제 됨
def delete_lesson(request, lesson_id):
    if not request.user.is_authenticated:
        return redirect('/login/')

    try:
        lesson_object = Lesson.objects.get(pk=lesson_id)
        # registration_objects = Registration.objects.filter(member_id=member_id)
        # registration_objects.delete()

        if lesson_object is not None:
            print('삭제 로그 기록')

            # 삭제 이력
            History.objects.create(
                lesson_id=lesson_object.id,
                lesson_date=lesson_object.lesson_date,
                lesson_time=lesson_object.lesson_time,
                created_by=request.user
            )

            lesson_object.delete()
    except Exception as e:
        print(e)
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
