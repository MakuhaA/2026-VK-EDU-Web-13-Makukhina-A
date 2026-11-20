from django.contrib.auth.password_validation import validate_password
from .models import Profile
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm


class LoginForms(AuthenticationForm):
    next = forms.CharField(widget=forms.HiddenInput(), required=False)
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if password == username:
            raise forms.ValidationError("Пароль и логин совпадают")

        return cleaned_data

    def cleaned_username(self):
        username = self.cleaned_data['username']
        if username == 'test':
            raise forms.ValidationError('Test')

        return username



class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise ValidationError("Пользователь с таким логином уже существует.")

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже зарегистрирован.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if password:
            try:
                validate_password(password, user=None)
            except ValidationError as e:
                raise forms.ValidationError(e.messages)

        return password

    def save(self):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user


from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    username = forms.CharField(label="Login", max_length=150, required=True)
    email = forms.EmailField(label="Email address", required=False)

    class Meta:
        model = Profile
        fields = ('avatar',)
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email

        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['avatar'].widget.attrs.update({'style': 'display: none;'})

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user

        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            profile.save()

        return profile