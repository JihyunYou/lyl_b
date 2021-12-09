from crispy_forms.bootstrap import InlineRadios
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div
from django import forms
from django.db.models import Max
from django.forms import ModelForm
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from .models import Member, Registration
from lessons.models import Attendance
from custom_users.models import User


class CustomMemberForm(forms.Form):
    name = forms.CharField(max_length=20, required=True)
    teacher_id = forms.ModelMultipleChoiceField(
        widget=forms.SelectMultiple(), queryset=User.objects.filter(user_grade=3))


# member form 초기 설정 (crispy)
class MemberForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(MemberForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-3'
        self.helper.field_class = 'col-9'
        self.helper.add_input(Submit('submit', '등록', css_class='btn-success'))
        self.helper.form_method = 'POST'

    class Meta:
        model = Member
        fields = '__all__'
        labels = {
            'name': '이름',
            'gender': '성별',
            'date_of_birth': '생년월일',
            'phone_number': '전화번호',
            'teacher_id': '담당강사'
        }


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


def index(request):
    member_objects = Member.objects.all()

    return render(
        request,
        'members/member_index.html',
        {
            'member_objects': member_objects
        }
    )


def detail(request, member_id):
    try:
        member_object = Member.objects.get(pk=member_id)
        registration_objects = Registration.objects.filter(member_id=member_id)
        attendance_objects = Attendance.objects.filter(member_id=member_id)

        # 회원 정보 수정
        form = MemberForm(request.POST or None, instance=member_object)
        if form.is_valid():
            form.save()
            return redirect(detail, member_id=member_id)

        # 회원권 등록
        registration_form = RegistrationFrom(request.POST or None)
        if registration_form.is_valid():
            registration = registration_form.save(commit=False)
            registration.member_id = member_object
            registration.save()
            return redirect(detail, member_id=member_id)

    except:
        raise Http404("존재하지 않는 회원입니다.")
    return render(
        request,
        'members/member_detail.html',
        {
            'member_object': member_object,
            'registration_objects': registration_objects,
            'attendance_objects': attendance_objects,
            'form': form,
            'registration_form': registration_form,
            'remaining_count': cal_remaining(member_id)
        }
    )


def delete_registration(request, member_id, registration_id):
    try:
        registration_object = Registration.objects.get(pk=registration_id)
        registration_object.delete()
    except:
        raise Http404("존재하지 않는 결재정보 입니다.")

    return redirect(detail, member_id=member_id)


def delete_member(request, member_id):
    try:
        member_object = Member.objects.get(pk=member_id)
        registration_objects = Registration.objects.filter(member_id=member_id)
        registration_objects.delete()
        member_object.delete()
    except:
        raise Http404("존재하지 않는 회원입니다.")

    return redirect('/member/')


def create_member(request):
    member_form = MemberForm

    if request.POST:
        member_form = MemberForm(request.POST)
        if member_form.is_valid():
            member = member_form.save()
            return redirect(detail, member_id=member.id)

    return render(
        request,
        'members/member_create.html',
        {
            'member_form': member_form
        }
    )


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