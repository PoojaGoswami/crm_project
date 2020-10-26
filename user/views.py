from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    return render(request, 'user/home.html')


from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from user.forms import SignUpForm, LoginForm
from django.contrib.auth import logout


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.athlete_code = form.cleaned_data.get('athlete_code')
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
            # form.save()
            # username = form.cleaned_data.get('username')
            # raw_password = form.cleaned_data.get('password1')
            # user = authenticate(username=username, password=raw_password)
            # login(request, user)
            # return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'user/signup.html', {'form': form})


# def login(request):
#     username = request.POST['username']
#     password = request.POST['password']
#     # athlete_code = request.POST['athlete_code']
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#         return redirect('home')
#
#     else:
#         form = LoginForm()


def logout(request):
    # logout(request)
    return redirect('login')
