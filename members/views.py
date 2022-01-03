from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput
from django.forms import ModelForm, formset_factory, inlineformset_factory, NumberInput
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from .models import Member, Registration, DefaultSchedule
from lessons.models import Attendance


# member form 초기 설정 (crispy)
class MemberForm(ModelForm):
    class Meta:
        model = Member
        fields = [
            'name', 'teacher_id', 'gender', 'date_of_birth', 'phone_number'
        ]
        labels = {
            'name': '이름',
            'gender': '성별',
            'date_of_birth': '생년월일',
            'phone_number': '전화번호',
            'teacher_id': '담당강사'
        }
        widgets = {
            'date_of_birth': DatePickerInput(
                options={
                    'format': 'YYYY-MM-DD',
                    'locale': 'ko',
                    'defaultDate': '2000-01-01'
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(MemberForm, self).__init__(*args, **kwargs)
        self.fields['date_of_birth'].required = False
        self.fields['phone_number'].required = False


class DefaultScheduleForm(ModelForm):
    class Meta:
        model = DefaultSchedule
        fields = [
            'day_of_week', 'lesson_time'
        ]
        labels = {
            'day_of_week': '요일',
            'lesson_time': '시간'
        }
        widgets = {
            'lesson_time': TimePickerInput(
                options={
                    'stepping': 10,
                }
            ),
        }


MemberDefaultScheduleFormset = inlineformset_factory(
    Member,
    DefaultSchedule,
    form=DefaultScheduleForm,
    min_num=0,
    max_num=2,
)


# registration form 초기 설정
class RegistrationFrom(ModelForm):
    class Meta:
        model = Registration
        fields = [
            'times', 'tuition', 'reg_date'
        ]
        labels = {
            'times': '등록 횟수',
            'tuition': '결제 금액',
            'reg_date': '결제 일자',
        }
        widgets = {
            'tuition': NumberInput(
                attrs={
                    'step': '1000'
                }
            ),
            'reg_date': DatePickerInput(
                options={
                    'format': 'YYYY-MM-DD',
                    'locale': 'ko'
                }
            ),
        }


def index(request):
    context = {}

    member_objects = Member.objects.all()
    context['member_objects'] = member_objects

    member_form = MemberForm
    defaultSchedule_formset = MemberDefaultScheduleFormset

    if request.POST:
        member_form = MemberForm(request.POST)
        if member_form.is_valid():
            member = member_form.save()

            default_schedule = MemberDefaultScheduleFormset(
                request.POST, instance=member
            )

            if default_schedule.is_valid():
                default_schedule.save()
            else:
                print(default_schedule.errors)

            return redirect(detail, member_id=member.id)
        else:
            print(member_form.errors)

    context['member_form'] = member_form
    context['defaultSchedule_formset'] = defaultSchedule_formset

    return render(
        request,
        'members/member_index.html',
        context
    )


def detail(request, member_id):
    try:
        # Data Load
        member_object = Member.objects.get(pk=member_id)
        default_schedule_objects = DefaultSchedule.objects.filter(member_id=member_id)
        registration_objects = Registration.objects.filter(member_id=member_id)
        attendance_objects = Attendance.objects.filter(member_id=member_id)

        # Form Init
        member_form = MemberForm(request.POST or None, instance=member_object)
        defaultSchedule_formset = MemberDefaultScheduleFormset(request.POST or None, instance=member_object)
        registration_form = RegistrationFrom(request.POST or None)

        # Member Update
        if member_form.is_valid():
            member_form.save()

            # Default Schedule Update
            if defaultSchedule_formset.is_valid():
                defaultSchedule_formset.save()

            return redirect(detail, member_id=member_id)

        # Registration Update
        if registration_form.is_valid():
            registration = registration_form.save(commit=False)
            registration.member_id = member_object
            registration.save()
            return redirect(detail, member_id=member_id)

    except:
        raise Http404("존재하지 않는 회원입니다.")

    finally:
        context = {}
        context['member_object'] = member_object
        context['default_schedule_objects'] = default_schedule_objects
        context['registration_objects'] = registration_objects
        context['attendance_objects'] = attendance_objects

        context['member_form'] = member_form
        context['defaultSchedule_formset'] = defaultSchedule_formset
        context['registration_form'] = registration_form

        context['remaining_count'] = cal_remaining(member_id)

    return render(
        request,
        'members/member_detail.html',
        context
    )


def delete_registration(request, member_id, registration_id):
    # 로그인 하지 않은 사용자가 URL을 통해 회원을 삭제하는 것을 막음
    if not request.user.is_authenticated:
        print("권한 없는 사용자")
        return redirect('/')

    try:
        registration_object = Registration.objects.get(pk=registration_id)
        registration_object.delete()
    except:
        raise Http404("존재하지 않는 결재정보 입니다.")

    return redirect(detail, member_id=member_id)


def delete_member(request, member_id):
    # 로그인 하지 않은 사용자가 URL을 통해 회원을 삭제하는 것을 막음
    if not request.user.is_authenticated:
        print("권한 없는 사용자")
        return redirect('/')

    try:
        member_object = Member.objects.get(pk=member_id)
        registration_objects = Registration.objects.filter(member_id=member_id)
        registration_objects.delete()
        member_object.delete()
    except:
        raise Http404("존재하지 않는 회원입니다.")

    return redirect('/member/')


def cal_remaining(member_id):
    total_count = 0
    registration_objects = Registration.objects.filter(member_id=member_id)
    for registration in registration_objects:
        total_count += registration.times

    attendance_objects = Attendance.objects.filter(member_id=member_id)
    for attendance in attendance_objects:
        if attendance.status == 1 or attendance.status == 3:
            total_count -= 1

    return total_count


class MemberCreate(CreateView):
    model = Member
    fields = [
        'name', 'gender', 'date_of_birth', 'phone_number', 'teacher_id',
        'mon_yn', 'mon_time',
        'tue_yn', 'tue_time',
        'wed_yn', 'wed_time',
        'thu_yn', 'thu_time',
        'fri_yn', 'fri_time',
        'sat_yn', 'sat_time',
    ]

    def form_valid(self, form):
        return super(MemberCreate, self).form_valid(form)

    # def get_success_url(self):
    #     return redirect('/member/')
