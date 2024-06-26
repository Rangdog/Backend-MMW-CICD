from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import CustomUser


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = CustomUser
        fields = ("username",)

    def clean_password2(self):
        # Kiểm tra hai mật khẩu có khớp nhau không
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Lưu mật khẩu đã được mã hóa vào database
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ("username", "password", "is_active", "is_superuser")

    def clean_password(self):
        # Bảo vệ mật khẩu, trả về giá trị ban đầu
        return self.initial["password"]

    def confirm_login_allowed(self, user):
        if not user.is_staff():
            raise forms.ValidationError(
                "This account is inactive.",
                code="inactive",
            )
