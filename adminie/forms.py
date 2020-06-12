from django import forms
from django.contrib.auth.models import User

from property.models import Property


class PropertyForm(forms.ModelForm):

    class Meta:
        model = Property
        exclude = ('property_id', 'added_at', 'added_by', 'bought', 'status', 'client_requests')
        # widgets = {
        #     # 'gallery': forms.ClearableFileInput(attrs={'multiple': True})
        # }


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')
