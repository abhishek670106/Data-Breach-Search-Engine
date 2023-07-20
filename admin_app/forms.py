from django import forms
from django.contrib.auth.models import User
from .models import AdminModel, UserProfile

import random
import string
from django import forms
from .models import AdminModel
from .models import AdminModel



class RedeemCodeForm(forms.ModelForm):
    num_codes = forms.IntegerField(label='Number of Codes', min_value=1)
    class Meta:
        model = AdminModel
        fields = ['value']

    def generate_unique_code(self):
        code_length = 8
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=code_length))
            if not AdminModel.objects.filter(code=code).exists():
                return code

    def generate_random_value(self):
        min_value = 10
        max_value = 100
        return random.randint(min_value, max_value)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.code = self.generate_unique_code()
        instance.value = self.generate_random_value()
        if commit:
            instance.save()
        return instance

    def generate_codes(self, num_codes):
        codes = []
        for _ in range(num_codes):
            code = self.generate_unique_code()
            value = self.generate_random_value()
            codes.append((code, value))
        return codes

    def clean(self):
        cleaned_data = super().clean()
        num_codes = cleaned_data.get('num_codes')
        if num_codes is not None and num_codes <= 0:
            raise forms.ValidationError("Number of codes must be greater than zero.")


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_pic']


class ChangePasswordForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data
