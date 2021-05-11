from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
                                       SetPasswordForm)

class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(label='Enter Firstname',min_length=1, max_length=10, help_text='Optional',required=False)
    last_name = forms.CharField(label='Enter Lastname',min_length=1, max_length=20, help_text='Optional',required=False)
    username = forms.CharField(label='Enter Username',min_length=3, max_length=20, help_text='Required')
    email = forms.EmailField(label='Enter Email',help_text='Required')
    password = forms.CharField(label='Enter Password',help_text='Required',widget=forms.PasswordInput,validators=[validate_password])
    class Meta:
        model = User
        fields = ('first_name','last_name','username','email',)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username = username)
        if r.count():
            raise forms.ValidationError('Username already exists')
        return username
    def clean_password(self):
        cd = self.cleaned_data
        if len(cd['password']) < 8:
            raise forms.ValidationError('Passwords should be 8 Characters')
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Please use another Email, that is already taken')
        return email
    

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['user_name'].widget.attrs.update(
    #         {'class': 'form-control mb-3', 'placeholder': 'Username'})
    #     self.fields['email'].widget.attrs.update(
    #         {'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
    #     self.fields['password'].widget.attrs.update(
    #         {'class': 'form-control mb-3', 'placeholder': 'Password'})
        

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))


class UserEditForm(forms.ModelForm):

    email = forms.EmailField(
        label='Account email (can not be changed)', max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'email', 'id': 'form-email', 'readonly': 'readonly'}))

    username = forms.CharField(
        label='username', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Username', 'id': 'form-firstname', 'readonly': 'readonly'}))

    first_name = forms.CharField(
        label='firstName', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Firstname', 'id': 'form-firstname'}))
    last_name = forms.CharField(
        label='LastName', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Lastname', 'id': 'form-lastname'}))

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].required = True
        self.fields['email'].required = True



class PwdResetForm(PasswordResetForm):

    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        u = User.objects.filter(email=email)
        if not u:
            raise forms.ValidationError(
                'Unfortunatley we can not find that email address')
        return email


class PwdResetConfirmForm(forms.Form):
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput())
            # attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput())
            # attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-new-pass2'}))
    user_email = forms.CharField()
    
    def update(self,user_password1,user):   
        try:
            
            if user.set_password(user_password1):
                user.save()
                return 'success'
            else:
                return 'fail'
        except Exception as e:
            print('form error',e)
            return 'fail'
