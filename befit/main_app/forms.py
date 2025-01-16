from django.forms import ModelForm, RadioSelect
from .models import Profile

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['age', 'gender', 'weight', 'height', 'image']
        widgets = {
            'gender': RadioSelect,
        }