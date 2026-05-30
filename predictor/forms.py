from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class PredictionForm(forms.Form):
    GENDER_CHOICES = [
        ("", "Select gender"),
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    ]

    YES_NO_CHOICES = [("True", "Yes"), ("False", "No")]

    name = forms.CharField(max_length=120)
    age = forms.IntegerField(min_value=1, max_value=120)
    gender = forms.ChoiceField(choices=GENDER_CHOICES)

    jaundice = forms.ChoiceField(choices=YES_NO_CHOICES, widget=forms.RadioSelect)
    abdominal_pain = forms.ChoiceField(choices=YES_NO_CHOICES, widget=forms.RadioSelect)
    weight_loss = forms.ChoiceField(choices=YES_NO_CHOICES, widget=forms.RadioSelect)
    fatigue = forms.ChoiceField(choices=YES_NO_CHOICES, widget=forms.RadioSelect)
    fever = forms.ChoiceField(choices=YES_NO_CHOICES, widget=forms.RadioSelect)

    bilirubin = forms.FloatField(min_value=0)
    alt = forms.FloatField(min_value=0)
    ast = forms.FloatField(min_value=0)
    alp = forms.FloatField(min_value=0)
    ca19_9 = forms.FloatField(min_value=0, label="CA 19-9")

    smoking = forms.ChoiceField(choices=YES_NO_CHOICES, widget=forms.RadioSelect)
    alcohol = forms.ChoiceField(choices=YES_NO_CHOICES, widget=forms.RadioSelect)
    diabetes = forms.ChoiceField(choices=YES_NO_CHOICES, widget=forms.RadioSelect)
    liver_disease_history = forms.ChoiceField(choices=YES_NO_CHOICES, widget=forms.RadioSelect)
    gallstones = forms.ChoiceField(choices=YES_NO_CHOICES, widget=forms.RadioSelect)

    def clean_name(self):
        value = self.cleaned_data["name"].strip()
        if len(value) < 2:
            raise forms.ValidationError("Invalid input: name must have at least 2 characters.")
        return value


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
