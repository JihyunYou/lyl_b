import datetime

from crispy_forms.helper import FormHelper
from django.forms import ModelForm, inlineformset_factory
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import CreateView

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
    return redirect('')


def create_manual_schedule(request):
    lesson_form = LessonForm
    attendance_formset = LessonAttendanceFormset

    if request.POST:
        lesson_form = LessonForm(request.POST)
        if lesson_form.is_valid():
            lesson = lesson_form.save()
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


# 시간 계산은 dummy 일자를 붙여 계산한 후 시간 추출하는 방식 사용
def cal_end_time(start_time):
    end_time = datetime.datetime(100, 1, 1, start_time.hour, start_time.minute, start_time.second)
    end_time = end_time + datetime.timedelta(minutes=50)
    return end_time.time()
