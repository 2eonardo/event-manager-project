from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import CustomUser
from .forms import SignupForm, ProfileEditForm  # <--- Import dei nuovi form
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
    """Vista per la registrazione con validazione automatica del Form"""
    if request.user.is_authenticated:
        return redirect('event_list')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()  # Crea l'utente e cripta la password automaticamente
            login(request, user)
            messages.success(request, 'Registrazione effettuata con successo! Benvenuto!')
            return redirect('event_list')
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})


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
        organized_events = user.organized_events.all()
        context = {'organized_events': organized_events}
    else:
        attended_events = user.registrations.all()
        context = {'attended_events': attended_events}
    return render(request, 'profile.html', context)


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def profile_edit_view(request):
    """Vista per modificare il profilo con ProfileEditForm"""
    user = request.user
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profilo aggiornato con successo!')
            return redirect('profile')
    else:
        form = ProfileEditForm(instance=user)

    return render(request, 'profile_edit.html', {'form': form})