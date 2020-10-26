from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    username = forms.CharField(max_length=30, required=False, help_text='Optional.', widget= forms.TextInput(attrs={'placeholder':'Name'}))
    birth_date = forms.CharField(max_length=30, required=False, help_text='Optional.', widget=forms.TextInput(attrs={'placeholder':'Date of birth'}))
    athlete_code = forms.CharField(max_length=150, required=False, help_text='Optional.', widget=forms.TextInput(attrs={'placeholder':'Athlete Code'}))
    address = forms.CharField(max_length=30, required=False, help_text='Optional.', widget=forms.TextInput(attrs={'placeholder':'Address'}))
    mobile = forms.CharField(max_length=30, required=False, help_text='Optional.', widget=forms.TextInput(attrs={'placeholder':'Mobile No.'}))
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.', widget=forms.TextInput(attrs={'placeholder':'Email'}))
    # birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD', widget=forms.TextInput(attrs={'placeholder':'Address'}))

    class Meta:
        model = User
        # fields = ('username', 'birth_date', 'first_name', 'last_name', 'email', 'password1', 'password2', )
        fields = ('username', 'birth_date', 'athlete_code', 'address', 'mobile', 'email' )


class LoginForm:
    username = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    password = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'placeholder': 'Name'}))
