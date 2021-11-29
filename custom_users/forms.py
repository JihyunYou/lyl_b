from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User

# admin.py 에서 필드 설정이 다 되는데 이건 왜 필요한 것인가??

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User   # 어떤 모델을 기반으로 한 입력공간인가
        # fields = ('email', 'password', 'full_name')     # 그 모델에서 어떤 항목을 입력받을 것인가
        fields = '__all__'

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        # fields = ('email',)
        fields = '__all__'
