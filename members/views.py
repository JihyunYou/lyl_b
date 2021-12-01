from django.http import Http404
from django.shortcuts import render
from .models import Member


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
    except:
        raise Http404("존재하지 않는 회원입니다.")
    return render(
        request,
        'members/member_detail.html',
        {
            'member_object': member_object
        }
    )