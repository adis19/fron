from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from users.models import Profile
from .userforms import UserRegisterForm
from django.contrib.auth import authenticate, logout as user_logout # База для входа и выхода с учетной записи
from django.contrib.auth import login
from django.contrib.auth.models import User  # База для авторизации
from .userforms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Ваш аккаунт создан: можно войти на сайт.')
            return redirect('loginPage')
    else:
        form = UserRegisterForm()
    return render(request, 'userregister.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Ваш профиль успешно обновлен.')
            return redirect('profile')
        
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request,'profile.html', context)


def u_login(request):
    if request.method == 'POST':  # Метод "POST" для отправки запроса вводом пользователя
        username = request.POST.get('username') 
        password = request.POST.get('password')

        try:  # Функция authenticate() для установки соответствия с именнем и паролем
            user = User.objects.get(username=username)
            user = authenticate(request, username=username, password=password)

            if user is not None:  # Если пользователь не <<Не найден>>, то перенаправляет в указанный .html
                login(request, user)
                return redirect('home_page')
            else:  # Отображение сообщения ошибки через метод .error()
                messages.error(request, "Invalid password.")
        except User.DoesNotExist:
            messages.error(request, "User does not exist.")

    return render(request, 'userlogin.html')


def logout(request):
    user_logout(request)
    return render(request,'userlogout.html')