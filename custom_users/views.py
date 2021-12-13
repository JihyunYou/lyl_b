from django.contrib import auth
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect

import lessons.views


def login(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect(lessons.views.index)
        else:
            return render(
                request,
                'login.html',
                {
                    'error': '로그인 정보가 잘못되었습니다'
                }
            )

    else:
        return render(request, 'login.html')


def logout(request):
    print('로그아웃 method')
    auth.logout(request)
    return redirect(lessons.views.index)


def about(request):
    return render(
        request,
        'about.html'
    )
