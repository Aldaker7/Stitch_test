from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)
from .models import StitchList, StitchCard, StitchBoard, Members

User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Username or Password incorrect")
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserSignupForm(forms.ModelForm):
    password2 = forms.CharField(label='Password confirmation',
                                widget=forms.PasswordInput)
    email1 = forms.EmailField(label='Email')
    email2 = forms.EmailField(label='Email confirmation')

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name',
                  'password', 'password2', 'email1', 'email2',)

    def save(self, commit=True):
        # Save the provided password in hashed format

        user = super().save(commit=False)
        if self.cleaned_data.get("email1") != self.cleaned_data.get("email2"):
            return forms.ValidationError("emails mismatching")
        if commit:
            user.set_password(self.cleaned_data.get("password"))
            user.save()
        return user

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2


class BoardForm(forms.ModelForm):
    class Meta:
        model = StitchBoard
        fields = ("title",)


class ListForm(forms.ModelForm):
    class Meta:
        model = StitchList
        fields = ('title',)


class CardForm(forms.ModelForm):
    class Meta:
        model = StitchCard
        fields = ('title', 'description', 'DueDate', 'member')


class MemberForm(forms.ModelForm):
    class Meta:
        model = Members
        fields = ('name',)
