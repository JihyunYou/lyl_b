from django.shortcuts import render


def about(request):
    return render(
        request,
        'common_app/about.html'
    )
