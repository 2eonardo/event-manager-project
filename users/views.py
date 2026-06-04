from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import CustomUser
from events.models import Registration


@require_http_methods(["GET", "POST"])
def login_view(request):
    """Vista per il login"""
    if request.user.is_authenticated:
        return redirect('event_list')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Benvenuto {user.username}!')
            return redirect('event_list')
        else:
            messages.error(request, 'Username o password non validi.')

    return render(request, 'login.html')


@require_http_methods(["GET", "POST"])
def signup_view(request):
    """Vista per la registrazione"""
    if request.user.is_authenticated:
        return redirect('event_list')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        bio = request.POST.get('bio', '')
        role = request.POST.get('role')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Validazioni
        if not username or not email or not password1 or not password2 or not role:
            messages.error(request, 'Compilare tutti i campi obbligatori.')
            return render(request, 'signup.html')

        if password1 != password2:
            messages.error(request, 'Le password non coincidono.')
            return render(request, 'signup.html')

        if len(password1) < 8:
            messages.error(request, 'La password deve contenere almeno 8 caratteri.')
            return render(request, 'signup.html')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username già in uso.')
            return render(request, 'signup.html')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email già registrata.')
            return render(request, 'signup.html')

        # Creare l'utente
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name,
            bio=bio,
            role=role
        )

        # Login automatico dopo registrazione
        login(request, user)
        messages.success(request, 'Registrazione effettuata con successo! Benvenuto!')
        return redirect('event_list')

    return render(request, 'signup.html')


@login_required(login_url='login')
def logout_view(request):
    """Vista per il logout"""
    logout(request)
    messages.success(request, 'Logout effettuato con successo.')
    return redirect('login')


@login_required(login_url='login')
def profile_view(request):
    """Vista per visualizzare il profilo dell'utente"""
    user = request.user

    if user.role == 'organizer':
        # Gli organizzatori vedono i loro eventi creati
        organized_events = user.organized_events.all()
        context = {
            'organized_events': organized_events,
        }
    else:
        # I partecipanti vedono i loro ticket
        attended_events = user.registrations.all()
        context = {
            'attended_events': attended_events,
        }

    return render(request, 'profile.html', context)


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def profile_edit_view(request):
    """Vista per modificare il profilo"""
    user = request.user

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email')
        bio = request.POST.get('bio', '')

        if not email:
            messages.error(request, 'Email è obbligatoria.')
            return render(request, 'profile_edit.html')

        # Verificare che l'email non sia già in uso
        if CustomUser.objects.filter(email=email).exclude(id=user.id).exists():
            messages.error(request, 'Email già in uso.')
            return render(request, 'profile_edit.html')

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.bio = bio
        user.save()

        messages.success(request, 'Profilo aggiornato con successo!')
        return redirect('profile')

    return render(request, 'profile_edit.html')
