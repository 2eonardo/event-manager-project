from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from datetime import datetime
from .models import Event, Registration, Category
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model
User = get_user_model()


@login_required(login_url='login')
def event_list(request):
    """Vista per visualizzare e filtrare gli eventi"""
    events = Event.objects.all()
    categories = Category.objects.all()


    # Filtro per categoria
    category_id = request.GET.get('category')
    if category_id:
        events = events.filter(category_id=category_id)
        selected_category = get_object_or_404(Category, id=category_id)
    else:
        selected_category = None

    # Filtro per data (singolo giorno)
    date = request.GET.get('date')
    date_obj = None
    if date:
        try:
            # Considera l'intero giorno: da 00:00:00 a 23:59:59
            parsed_dt = datetime.strptime(date, '%Y-%m-%d')
            start_of_day = parsed_dt.replace(hour=0, minute=0, second=0)
            end_of_day = parsed_dt.replace(hour=23, minute=59, second=59)
            events = events.filter(date__gte=start_of_day, date__lte=end_of_day)
            # Passiamo un oggetto date/datetime al template per poterlo formattare con il filtro |date
            date_obj = parsed_dt.date()
        except ValueError:
            date = None

    # Filtro per luogo (ricerca testuale, case-insensitive)
    location = request.GET.get('location')
    if location:
        events = events.filter(location__icontains=location)

    # Ordinamento per data
    order = request.GET.get('order')
    if order == 'desc':
        events = events.order_by('-date')
        order_by = "Eventi più lontani"
    elif order == 'asc':
        events = events.order_by('date')
        order_by = "Eventi immediati"
    else:
        # Default ordering (da models.py: ordering = ['date'])
        order_by = None

    context = {
        'events': events,
        'categories': categories,
        'selected_category': selected_category,
        'date': date,
        'date_obj': date_obj,
        'location': location,
        'order_by': order_by,
        'active_filters': bool(category_id or date or location or order),
    }

    return render(request, 'event_list.html', context)


@login_required(login_url='login')
def event_detail(request, pk):
    """Vista per visualizzare i dettagli di un evento"""
    event = get_object_or_404(Event, pk=pk)
    is_registered = False

    if request.user.is_authenticated:
        is_registered = Registration.objects.filter(
            event=event,
            attendee=request.user
        ).exists()

    context = {
        'event': event,
        'is_registered': is_registered,
    }

    return render(request, 'event_detail.html', context)


@login_required(login_url='login')
def event_create(request):
    """Vista per creare un nuovo evento (solo organizzatori)"""
    # Verificare che l'utente sia un organizzatore
    if request.user.role != 'organizer':
        messages.error(request, 'Solo gli organizzatori possono creare eventi.')
        return redirect('event_list')

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        date_str = request.POST.get('date')
        location = request.POST.get('location')
        category_id = request.POST.get('category')

        # Validazione basica
        if not all([title, description, date_str, location]):
            messages.error(request, 'Si prega di compilare tutti i campi obbligatori.')
            return render(request, 'event_form.html', {'categories': Category.objects.all()})

        try:
            date = datetime.fromisoformat(date_str)
        except ValueError:
            messages.error(request, 'Formato data non valido.')
            return render(request, 'event_form.html', {'categories': Category.objects.all()})

        # Creare l'evento
        event = Event.objects.create(
            title=title,
            description=description,
            date=date,
            location=location,
            organizer=request.user,
            category_id=category_id if category_id else None
        )

        messages.success(request, 'Evento creato con successo!')
        return redirect('event_detail', pk=event.id)

    context = {
        'categories': Category.objects.all(),
    }

    return render(request, 'event_form.html', context)


@login_required(login_url='login')
def event_edit(request, pk):
    """Vista per modificare un evento"""
    event = get_object_or_404(Event, pk=pk)

    # Verificare che l'utente sia il proprietario
    if event.organizer != request.user:
        messages.error(request, 'Non hai il permesso di modificare questo evento.')
        return redirect('event_detail', pk=event.id)

    if request.method == 'POST':
        event.title = request.POST.get('title')
        event.description = request.POST.get('description')
        location = request.POST.get('location')
        date_str = request.POST.get('date')
        category_id = request.POST.get('category')

        if not all([event.title, event.description, location, date_str]):
            messages.error(request, 'Si prega di compilare tutti i campi obbligatori.')
            return render(request, 'event_form.html', {
                'form': type('obj', (object,), {'instance': event}),
                'categories': Category.objects.all(),
            })

        try:
            event.date = datetime.fromisoformat(date_str)
        except ValueError:
            messages.error(request, 'Formato data non valido.')
            return render(request, 'event_form.html', {
                'form': type('obj', (object,), {'instance': event}),
                'categories': Category.objects.all(),
            })

        event.location = location
        event.category_id = category_id if category_id else None
        event.save()

        messages.success(request, 'Evento modificato con successo!')
        return redirect('event_detail', pk=event.id)

    context = {
        'form': type('obj', (object,), {'instance': event}),
        'categories': Category.objects.all(),
    }

    return render(request, 'event_form.html', context)


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def event_delete(request, pk):
    """Vista per eliminare un evento"""
    event = get_object_or_404(Event, pk=pk)

    # Verificare che l'utente sia il proprietario
    if event.organizer != request.user:
        messages.error(request, 'Non hai il permesso di eliminare questo evento.')
        return redirect('event_detail', pk=event.id)

    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Evento eliminato con successo!')
        return redirect('event_list')

    # Se GET, mostra una pagina di conferma
    return render(request, 'event_confirm_delete.html', {'event': event})


@login_required(login_url='login')
@require_http_methods(["POST"])
def event_register(request, pk):
    """Vista per iscriversi a un evento"""
    event = get_object_or_404(Event, pk=pk)

    # Verificare che l'utente sia un partecipante
    if request.user.role != 'attendee':
        messages.error(request, 'Solo i partecipanti possono iscriversi agli eventi.')
        return redirect('event_detail', pk=event.id)

    # Verificare se già iscritto
    if Registration.objects.filter(event=event, attendee=request.user).exists():
        messages.info(request, 'Sei già iscritto a questo evento!')
        return redirect('event_detail', pk=event.id)

    # Creare la registrazione
    Registration.objects.create(event=event, attendee=request.user)
    messages.success(request, f'Iscrizione effettuata per "{event.title}"!')

    return redirect('event_detail', pk=event.id)


@login_required(login_url='login')
@require_http_methods(["POST"])
def event_unregister(request, pk):
    """Vista per annullare l'iscrizione a un evento"""
    event = get_object_or_404(Event, pk=pk)

    # Trovare e eliminare la registrazione
    registration = Registration.objects.filter(event=event, attendee=request.user).first()

    if registration:
        registration.delete()
        messages.success(request, f'Iscrizione annullata per "{event.title}"!')
    else:
        messages.info(request, 'Non eri iscritto a questo evento.')

    return redirect('event_detail', pk=event.id)


@login_required(login_url='login')
def organizer_events(request, organizer_id):
    """Vista per visualizzare tutti gli eventi creati da un organizzatore specifico"""
    # Verifica che l'organizzatore esista
    organizer = get_object_or_404(User, id=organizer_id, role='organizer')
    
    # Recupera tutti gli eventi dell'organizzatore ordinati per data decrescente (più recenti prima)
    events = Event.objects.filter(organizer=organizer).order_by('-date')
    
    context = {
        'organizer': organizer,
        'events': events,
    }
    
    return render(request, 'organizer_events.html', context)
