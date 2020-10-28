from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from user.forms import SignUpForm, LoginForm
from django.contrib.auth import logout

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string


from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Profile
from django.contrib import messages


@login_required
# @login_required(login_url='/login/')
def home(request):
    return render(request, 'user/home.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.signup_confirmation = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'user/activation_invalid.html')


def activation_sent_view(request):
    return render(request, 'user/activation_sent.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.athlete_code = form.cleaned_data.get('athlete_code')
            print('athlete_code', user.profile.athlete_code)
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.profile.email = form.cleaned_data.get('email')
            user.profile.mobile = form.cleaned_data.get('mobile')
            user.profile.address = form.cleaned_data.get('address')
            user.is_active = True
            user.save()
            # username = form.cleaned_data.get('username')
            # password = form.cleaned_data.get('password1')
            password = user.set_password(user.password)
            user = authenticate(username=user.username, password=password)
            login(request, user)
            return redirect('home')

            # current_site = get_current_site(request)
            # subject = 'Please Activate Your Account'
            # message = render_to_string('activation_request.html', {
            #     'user': user,
            #     'domain': current_site.domain,
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token': account_activation_token.make_token(user),
            # })
            # user.email_user(subject, message)
            # return redirect('activation_sent')
        else:
            form = SignUpForm()

    else:
        form = SignUpForm()

    return render(request, 'user/signup.html', {'form': form})


def login_user(request):
    print("helo")
    if request.method == "POST":
        print("hello")
        # form = AuthenticationForm(request=request, data=request.POST)
        form = LoginForm(data=request.POST)
        print('foem', form, form.is_valid())
        print(form.errors)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            athlete_code = form.cleaned_data.get('athlete_code')
            print('form', username, password, athlete_code)

            user = authenticate(username=username, password=password)
            print('user', user)
            if user is not None:
                if user.is_active:
                    athlete_code = Profile.objects.filter(athlete_code=athlete_code)
                    print('athlete_code', athlete_code)
                    if athlete_code:
                        login(request, user)
                        messages.info(request, f"You are now logged in as {username}")
                        return redirect('/')
                    else:
                        messages.error(request, "Invalid username or password.")
                        print("Invalid details.")
            else:
                messages.error(request, "Invalid user details")
                print("Invalid user details.")
    else:
        form = LoginForm()

    return render(request=request, template_name="user/login.html", context={"form":form})




def logout(request):
    # logout(request)
    return redirect('login')
