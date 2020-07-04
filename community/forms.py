from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Trade, UserProfile

class DateInput(forms.DateInput):
    input_type = 'date'

class TradeForm(ModelForm):
    class Meta:
        model = Trade
        widgets = {'openedpositionon': DateInput() }
        fields = ['description', 'pair', 'image', 'openedpositionon', 'winlose', 'pips', 'lotsize', 'amount']

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'image', 'traderlevel', 'gender', 'bio', 'country', 'instagram']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    class Meta:
        model = User
        fields = ['username', 'email']

class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=False)
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]