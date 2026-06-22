from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from datetime import datetime
from .models import Event, Registration, Category
from .forms import EventForm
from django.contrib.auth import get_user_model

User = get_user_model()


# --- MIXINS DI PERMESSO PERSONALIZZATI ---

class OrganizerRequiredMixin(UserPassesTestMixin):
    """Verifica che l'utente sia un organizzatore"""

    def test_func(self):
        return self.request.user.role == 'organizer'

    def handle_no_permission(self):
        messages.error(self.request, 'Operazione consentita solo agli organizzatori.')
        return redirect('event_list')


class EventOwnerRequiredMixin(UserPassesTestMixin):
    """Verifica che l'utente sia l'effettivo proprietario dell'evento"""

    def test_func(self):
        event = self.get_object()
        return self.request.user == event.organizer

    def handle_no_permission(self):
        messages.error(self.request, 'Non hai il permesso di modificare questo evento.')
        return redirect('event_list')


# --- VISTE DEL PROGETTO ---

# events/views.py

@login_required(login_url='login')
def event_list(request):
    """Visualizza e filtra gli eventi"""
    events = Event.objects.all()
    categories = Category.objects.all()

    category_id = request.GET.get('category')
    if category_id:
        events = events.filter(category_id=category_id)
        selected_category = get_object_or_404(Category, id=category_id)
    else:
        selected_category = None

    date = request.GET.get('date')
    date_obj = None
    if date:
        try:
            parsed_dt = datetime.strptime(date, '%Y-%m-%d')

            # Rendiamo gli orari di inizio e fine giornata consapevoli del fuso orario (make_aware)
            start_of_day = timezone.make_aware(parsed_dt.replace(hour=0, minute=0, second=0))
            end_of_day = timezone.make_aware(parsed_dt.replace(hour=23, minute=59, second=59))

            events = events.filter(date__gte=start_of_day, date__lte=end_of_day)
            date_obj = parsed_dt.date()
        except ValueError:
            date = None

    location = request.GET.get('location')
    if location:
        events = events.filter(location__icontains=location)

    order = request.GET.get('order')
    if order == 'desc':
        events = events.order_by('-date')
        order_by = "Eventi più lontani"
    elif order == 'asc':
        events = events.order_by('date')
        order_by = "Eventi immediati"
    else:
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
    """Visualizza il dettaglio di un singolo evento"""
    event = get_object_or_404(Event, pk=pk)
    is_registered = False

    if request.user.is_authenticated:
        is_registered = Registration.objects.filter(event=event, attendee=request.user).exists()

    context = {
        'event': event,
        'is_registered': is_registered,
    }
    return render(request, 'event_detail.html', context)


# --- CLASS-BASED VIEWS PER LE OPERAZIONI CRUD ---

class EventCreateView(LoginRequiredMixin, OrganizerRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'event_form.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.instance.organizer = self.request.user
        return form

    def form_valid(self, form):
        # Quando arriviamo qui, il controllo anti-duplicato è già passato con successo
        messages.success(self.request, 'Evento creato con successo!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('event_detail', kwargs={'pk': self.object.pk})

class EventUpdateView(LoginRequiredMixin, EventOwnerRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'event_form.html'

    def form_valid(self, form):
        messages.success(self.request, 'Evento modificato con successo!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('event_detail', kwargs={'pk': self.object.pk})


class EventDeleteView(LoginRequiredMixin, EventOwnerRequiredMixin, DeleteView):
    model = Event
    template_name = 'event_confirm_delete.html'
    success_url = reverse_lazy('event_list')

    def post(self, request, *args, **kwargs):
        messages.success(self.request, 'Evento eliminato con successo!')
        return super().post(request, *args, **kwargs)


# --- VISTE DI ISCRIZIONE ---

@login_required(login_url='login')
@require_http_methods(["POST"])
def event_register(request, pk):
    """Vista per iscriversi a un evento in modo atomico e sicuro"""
    event = get_object_or_404(Event, pk=pk)

    # 1. CONTROLLO EVENTO CONCLUSO: impedisci iscrizione se la data è passata
    if event.date < timezone.now():
        messages.error(request, 'Operazione negata. L’evento è già concluso.')
        return redirect('event_detail', pk=event.id)

    # 2. Verificare che l'utente sia un partecipante (attendee)
    if request.user.role != 'attendee':
        messages.error(request, 'Solo i partecipanti possono iscriversi agli eventi.')
        return redirect('event_detail', pk=event.id)

    # 3. Iscrizione atomica concorrente con get_or_create (evita crash di sistema)
    registration, created = Registration.objects.get_or_create(
        event=event,
        attendee=request.user
    )

    if created:
        messages.success(request, f'Iscrizione effettuata per "{event.title}"!')
    else:
        messages.info(request, 'Sei già iscritto a questo evento!')

    return redirect('event_detail', pk=event.id)

@login_required(login_url='login')
@require_http_methods(["POST"])
def event_unregister(request, pk):
    event = get_object_or_404(Event, pk=pk)
    registration = Registration.objects.filter(event=event, attendee=request.user).first()

    if registration:
        registration.delete()
        messages.success(request, f'Iscrizione annullata per "{event.title}"!')
    else:
        messages.info(request, 'Non eri iscritto a questo evento.')

    return redirect('event_detail', pk=event.id)


@login_required(login_url='login')
def organizer_events(request, organizer_id):
    organizer = get_object_or_404(User, id=organizer_id, role='organizer')
    events = Event.objects.filter(organizer=organizer).order_by('-date')
    context = {
        'organizer': organizer,
        'events': events,
    }
    return render(request, 'organizer_events.html', context)