from django.db.models import Max
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from .models import Member, Registration


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
    except:
        raise Http404("존재하지 않는 회원입니다.")
    return render(
        request,
        'members/member_detail.html',
        {
            'member_object': member_object,
            'registration_objects': registration_objects
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


class RegistrationCreate(CreateView):
    model = Registration
    fields = [
        'times', 'reg_date', 'tuition'
    ]

    def form_valid(self, form, **kwargs):
        member_object = Member.objects.get(id=self.kwargs['member_id'])
        form.instance.member_id = member_object
        # form.instance.reg_seq = Registration.objects.filter(member_id=self.kwargs['member_id']).aggregate(Max('reg_seq')) + 1

        return super(RegistrationCreate, self).form_valid(form)
