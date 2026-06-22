from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': "Titolo dell'evento"}),
            'description': forms.Textarea(attrs={'placeholder': "Descrizione dell'evento...", 'rows': 4}),
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'location': forms.TextInput(attrs={'placeholder': "Luogo dell'evento"}),
            'category': forms.Select(),
        }
        labels = {
            'title': "Titolo dell'Evento",
            'description': 'Descrizione',
            'date': 'Data e Ora',
            'location': 'Luogo',
            'category': 'Categoria',
        }