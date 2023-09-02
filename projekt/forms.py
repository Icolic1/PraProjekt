from django import forms
from .models import Obavijest, Kolegij, Profesor
from django.utils.timezone import now

class obavijestForm(forms.ModelForm):
    class Meta:
        model = Obavijest
        kolegij = forms.ModelChoiceField(queryset=Kolegij.objects.all(), empty_label=None, widget=forms.Select(attrs={'required': True}))
        fields = ['title', 'content', 'kolegij']




class kolegijForm(forms.ModelForm):
    class Meta:
        model = Kolegij
        profesor = forms.ModelChoiceField(queryset=Profesor.objects.all(), empty_label=None, widget=forms.Select(attrs={'required': True}))
        fields = ['kolegij_naziv', 'profesor']


class profesorForm(forms.ModelForm):
    class Meta:
        model = Profesor
        fields=[]
        
        