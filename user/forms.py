from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
# from django.contrib.admin.widgets import AdminDateWidget
# from django.forms.fields import DateField
from .widgets import FengyuanChenDatePickerInput


class SignUpForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        # self.fields['password'].widget.attrs['placeholder'] = 'Password'
        # self.fields['password1'].widget.attrs['placeholder'] = 'Confirm Password'

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    # username = forms.CharField(max_length=50, required=False, help_text='Optional.', widget= forms.TextInput(attrs={'placeholder':'Name'}))
    birth_date = forms.CharField(max_length=25, required=False, help_text='', widget=forms.TextInput(attrs={'placeholder':'Date of birth'}))
    # birth_date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])
    # birth_date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'], widget=FengyuanChenDatePickerInput())
    athlete_code = forms.CharField(max_length=50, required=False, help_text='', widget=forms.TextInput(attrs={'placeholder':'Athlete Code'}))
    address = forms.CharField(max_length=150, required=False, help_text='', widget=forms.TextInput(attrs={'placeholder':'Address'}))
    mobile = forms.CharField(max_length=30, required=False, help_text='', widget=forms.TextInput(attrs={'placeholder':'Mobile No.'}))
    email = forms.EmailField(max_length=50, help_text='Required. Inform a valid email address.', widget=forms.TextInput(attrs={'placeholder':'Email'}))

    class Meta:
        model = User
        fields = ('username', 'birth_date', 'athlete_code', 'address', 'mobile', 'email', 'password1', 'password2')


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        # self.fields['password'].widget.attrs['placeholder'] = 'Password'
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    athlete_code = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'placeholder': 'Athlete Code'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))

    class Meta:
        model = User
        fields = ('username', 'athlete_code', 'password')

