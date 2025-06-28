from django import forms
from .models import Profile
from django.contrib.auth.models import User

class SignupForm(forms.ModelForm):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('staff', 'Staff'),
          )

    email=forms.EmailField()
    password=forms.CharField(widget=forms.PasswordInput)
    role=forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
            model = User
            fields = ['username', 'email', 'password']

    def save(self, commit=True):
            user = super().save(commit=False)
            user.set_password(self.cleaned_data['password'])
            if commit:
                user.save()
                Profile.objects.create(user=user, role=self.cleaned_data['role'])
            return user
        

    
       