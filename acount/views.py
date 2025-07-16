from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import SignUpForm, LoginForm, ChangePassForm
from .utils import generic_code, send_to_mail
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            messages.success(request, 'Muvaffaqiyatli ro‘yxatdan o‘tildi.')
            return redirect('index')  
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Tizimga kirdingiz.')
            return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Chiqdingiz.')
    return redirect('login')

@login_required
def change_pass_view(request):
    if request.method == "GET":
        code = generic_code()
        request.session['verification_code'] = code
        send_to_mail(request.user.email, code)
        messages.info(request,'emailingizga kod yuborildi')
        form = ChangePassForm()
        return render(request, 'change.html',{'form':form})
    else:
        form = ChangePassForm(request.POST)
        if form.is_valid():
            old_pass = form.cleaned_data['ol_pass']
            new_pass = form.cleaned_data['new_pass']
            code = form.cleaned_data['code']
            session_code = request.session.get('verification_code')


            if not request.user.check_password(old_pass):
                messages.error(request, 'Siz eski parolingizni noto‘g‘ri kiritdingiz!')
                return redirect('change-pass') 

            
            if session_code != code:
                messages.error(request,'tastiqlash kodingiz xato')
                return redirect('change-pass')

            user = request.user
            user.set_password(new_pass)
            user.save()
            messages.success(request, 'Parolingiz o‘zgartirildi')
            return redirect('profile')