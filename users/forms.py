from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")
    first_name = forms.CharField(required=True, label="Nome")
    last_name = forms.CharField(required=True, label="Cognome")

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name', 'role', 'bio')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'role': 'Ruolo',
            'bio': 'Bio (opzionale)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aggiungiamo graficamente l'asterisco anche ai campi ereditati in automatico
        self.fields['username'].label = "Username"

    # --- CONTROLLO EMAIL DUPLICATE IN REGISTRAZIONE ---
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Questo indirizzo email è già registrato nel sistema.")
        return email


class ProfileEditForm(forms.ModelForm):
    """Form per la modifica dei dati personali dell'utente"""
    email = forms.EmailField(required=True, label="Email")
    first_name = forms.CharField(required=True, label="Nome")
    last_name = forms.CharField(required=True, label="Cognome")

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'bio': 'Bio',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Questo indirizzo email è già utilizzato da un altro account.")
        return email