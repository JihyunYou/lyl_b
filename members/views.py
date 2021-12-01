from django.db.models import Max
from django.http import Http404
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
        member_object = Member.objects.get(id=member_id)
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


class MemberCreate(CreateView):
    model = Member
    fields = [
        'name', 'gender', 'date_of_birth', 'phone_number', 'teacher_id'
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
