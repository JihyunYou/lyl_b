from django.shortcuts import render, redirect

from qna_app.models import Post, Comment


def index(request):
    post_objects = Post.objects.all()

    return render(
        request,
        'qna_app/qna_list.html',
        {
            'post_objects': post_objects
        }
    )


def create_qna(request):
    # 로그인 하지 않은 사용자가 URL을 통해 회원을 삭제하는 것을 막음
    if not request.user.is_authenticated:
        print("권한 없는 사용자")
        return redirect('/')

    if request.POST:
        title = request.POST['title']
        content = request.POST['content']

        post = Post.objects.create(
            title=title,
            content=content,
            created_by=request.user
        )

    return redirect(index)


def detail(request, post_id):
    post_object = Post.objects.get(pk=post_id)
    comment_objects = Comment.objects.filter(post_id=post_id)

    return render(
        request,
        'qna_app/qna_detail.html',
        {
            'post_object': post_object,
            'comment_objects': comment_objects
        }
    )


def create_comment(request, post_id):
    # 로그인 하지 않은 사용자가 URL을 통해 회원을 삭제하는 것을 막음
    if not request.user.is_authenticated:
        print("권한 없는 사용자")
        return redirect('/')

    if request.POST:
        comment = request.POST['comment']
        post_object = Post.objects.get(pk=post_id)

        comment_object = Comment.objects.create(
            post_id=post_object,
            comment=comment,
            created_by=request.user
        )

    return redirect(detail, post_id)