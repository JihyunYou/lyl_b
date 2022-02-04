from datetime import datetime

from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput, MonthPickerInput
from django import forms
from django.db.models import Q, Sum, Count
from django.forms import ModelForm, formset_factory, inlineformset_factory, NumberInput
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from .models import Member, Registration, DefaultSchedule
from lessons.models import Attendance
from dal import autocomplete


# member form 초기 설정 (crispy)
class MemberForm(ModelForm):
    class Meta:
        model = Member
        fields = [
            'name', 'teacher_id', 'status', 'gender', 'date_of_birth', 'phone_number'
        ]
        labels = {
            'name': '이름',
            'gender': '성별',
            'date_of_birth': '생년월일',
            'phone_number': '전화번호',
            'teacher_id': '담당강사',
            'status': '회원권'
        }
        widgets = {
            'date_of_birth': DatePickerInput(
                options={
                    'format': 'YYYY-MM-DD',
                    'locale': 'ko',
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
            'times', 'tuition', 'payment', 'reg_date', 'description'
        ]
        labels = {
            'times': '등록 횟수',
            'tuition': '결제 금액',
            'payment': '결제 수단',
            'reg_date': '결제 일자',
            'description': '비고'
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

    def __init__(self, *args, **kwargs):
        super(RegistrationFrom, self).__init__(*args, **kwargs)
        self.fields['description'].required = False


# 회원 Autocomplete
class MemberAutocompelete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Member.objects.all()

        if self.q:
            qs = qs.filter(name__contains=self.q)

        return qs


class RegistrationForm2(ModelForm):
    class Meta:
        model = Registration
        fields = [
            'member_id', 'times', 'tuition', 'payment', 'reg_date', 'description'
        ]
        labels = {
            'member_id': '회원',
            'times': '등록 횟수',
            'tuition': '결제 금액',
            'payment': '결제 수단',
            'reg_date': '결제 일자',
            'description': '비고'
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
            'member_id': autocomplete.ModelSelect2(url='member-autocomplete')
        }

    def __init__(self, *args, **kwargs):
        super(RegistrationForm2, self).__init__(*args, **kwargs)
        self.fields['description'].required = False


class DateForm(forms.Form):
    input_date = forms.DateField(
        input_formats=['%Y-%m-%d'],
        label='조회할 월을 고르세요',
        widget=MonthPickerInput(
            attrs={
                'id': 'input_date',
            },
            options={
                'format': 'YYYY-MM',
                'locale': 'ko',
            }
        )
    )


def index(request):
    context = {}

    active_member_objects = Member.objects.filter(status=1)
    context['active_member_objects'] = active_member_objects

    inactive_member_objects = Member.objects.filter(~Q(status=1))
    context['inactive_member_objects'] = inactive_member_objects

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

            count = Registration.objects.filter(member_id=member_object).count()
            print(count)
            registration.reg_seq = count + 1

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


def registration_list(request):
    if not request.user.is_authenticated:
        return redirect('/login/')

    context = {}

    date_form = DateForm
    if request.POST:
        input_date = request.POST['input_date'].split('-')
        load_year = input_date[0]
        load_month = input_date[1]
    else:
        load_year = datetime.today().year
        load_month = datetime.today().month

    registrations = Registration.objects.filter(
        reg_date__year=load_year,
        reg_date__month=load_month
    )

    bank_count = registrations.filter(payment=1).aggregate(
        count=Count('tuition')
    ).get('count') or 0
    bank_total = registrations.filter(payment=1).aggregate(
        total=Sum('tuition')
    ).get('total') or 0

    cash_count = registrations.filter(payment=2).aggregate(
        count=Count('tuition')
    ).get('count') or 0
    cash_total = registrations.filter(payment=2).aggregate(
        total=Sum('tuition')
    ).get('total') or 0

    card_count = registrations.filter(payment=3).aggregate(
        count=Count('tuition')
    ).get('count') or 0
    card_total = registrations.filter(payment=3).aggregate(
        total=Sum('tuition')
    ).get('total') or 0

    context['date_form'] = date_form
    context['load_year'] = load_year
    context['load_month'] = load_month

    context['registrations'] = registrations

    context['bank_count'] = bank_count
    context['bank_total'] = bank_total
    context['cash_count'] = cash_count
    context['cash_total'] = cash_total
    context['card_count'] = card_count
    context['card_total'] = card_total

    context['all_cash_count'] = bank_count + cash_count
    context['all_cash_total'] = bank_total + cash_total

    context['all_count'] = bank_count + cash_count + card_count
    context['all_total'] = bank_total + cash_total + card_total

    return render(
        request,
        'members/registration_list.html',
        context
    )


def registration_detail(request, registration_id):
    if not request.user.is_authenticated:
        return redirect('/login/')

    context = {}

    registration = Registration.objects.get(pk=registration_id)
    registration_form = RegistrationFrom(request.POST or None, instance=registration)

    if request.POST:
        if registration_form.is_valid():
            registration_form.save()
            return redirect(registration_detail, registration_id)

    context['registration'] = registration
    context['registration_form'] = registration_form

    return render(
        request,
        'members/registration_detail.html',
        context
    )


def add_registration(request):
    if not request.user.is_authenticated:
        return redirect('/login/')

    context = {}

    registration_form = RegistrationForm2()

    # work 추가
    if request.POST:
        registration_form = RegistrationForm2(request.POST)
        if registration_form.is_valid():
            registration = registration_form.save(commit=False)

            count = Registration.objects.filter(member_id=registration.member_id).count()
            registration.reg_seq = count + 1

            registration.save()

            return redirect(registration_detail, registration.id)

    context['registration_form'] = registration_form

    return render(
        request,
        'members/registration_add.html',
        context
    )


def delete_registration(request, registration_id):
    if not request.user.is_authenticated:
        return redirect('/login/')

    try:
        registration = Registration.objects.get(pk=registration_id)

        del_reg_seq = registration.reg_seq

        registrations = Registration.objects.filter(member_id=registration.member_id.id)
        if del_reg_seq is None:
            for temp in registrations:
                if temp.reg_seq is not None:
                    temp.reg_seq -= 1
                    temp.save()
        else:
            for temp in registrations:
                if temp.reg_seq > del_reg_seq:
                    temp.reg_seq -= 1
                    temp.save()

        registration.delete()
    except:
        raise Http404("존재하지 않는 결재정보 입니다.")

    return redirect(registration_list)