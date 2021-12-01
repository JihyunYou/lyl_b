import datetime

from django.shortcuts import render
from .models import Lesson, Attendance, Member


# Create your views here.
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
            str(i.lesson_date) + ' ' + str(calEndTime(i.lesson_time)),
            "%Y-%m-%d %H:%M:%S"
        ).strftime("%Y-%m-%d %H:%M:%S")

        event_sub_arr['start'] = start_dt
        event_sub_arr['end'] = end_dt

        event_arr.append(event_sub_arr)

    return render(
        request,
        'lessons/index.html',
        {
            'lesson_objects': lesson_objects,
            'events': event_arr
        }
    )


# 시간 계산은 dummy 일자를 붙여 계산한 후 시간 추출하는 방식 사용
def calEndTime(start_time):
    end_time = datetime.datetime(100, 1, 1, start_time.hour, start_time.minute, start_time.second)
    end_time = end_time + datetime.timedelta(minutes=50)
    return end_time.time()
