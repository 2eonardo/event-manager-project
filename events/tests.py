from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse
from django.core.exceptions import ValidationError
from datetime import timedelta
from .models import Event, Category, Registration

User = get_user_model()


class EventSystemTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Tech")

        self.organizer1 = User.objects.create_user(
            username="demo_organizer1",
            email="organizer1@test.com",
            password="password123",
            role="organizer"
        )
        self.organizer2 = User.objects.create_user(
            username="demo_organizer2",
            email="organizer2@test.com",
            password="password123",
            role="organizer"
        )
        self.attendee = User.objects.create_user(
            username="demo_attendee1",
            email="attendee1@test.com",
            password="password123",
            role="attendee"
        )

        self.future_date = timezone.now() + timedelta(days=5)

    def test_create_valid_event_by_organizer(self):
        """Verifica che un organizzatore possa creare correttamente un evento"""
        self.client.login(username="demo_organizer1", password="password123")
        response = self.client.post(reverse('event_create'), {
            'title': 'Hackathon Università',
            'description': 'Descrizione hackathon',
            'date': self.future_date.strftime('%Y-%m-%dT%H:%M'),
            'location': 'Firenze',
            'category': self.category.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Event.objects.filter(title='Hackathon Università').exists())

    def test_prevent_duplicate_events_same_organizer(self):
        """Verifica il blocco di creazione di eventi identici dello stesso organizzatore"""
        Event.objects.create(
            title="Hackathon Università",
            description="Primo evento",
            date=self.future_date,
            location="Firenze",
            category=self.category,
            organizer=self.organizer1
        )

        event_duplicato = Event(
            title="Hackathon Università",
            description="Secondo evento identico",
            date=self.future_date,
            location="Firenze",
            category=self.category,
            organizer=self.organizer1
        )
        with self.assertRaises(ValidationError):
            event_duplicato.full_clean()

    def test_prevent_past_date_event(self):
        """Verifica il vincolo del modello che vieta date nel passato"""
        past_date = timezone.now() - timedelta(days=2)
        event = Event(
            title="Evento Obsoleto",
            description="Nel passato",
            date=past_date,
            location="Firenze",
            category=self.category,
            organizer=self.organizer1
        )
        with self.assertRaises(ValidationError):
            event.full_clean()

    def test_unauthorized_user_cannot_edit_event(self):
        """Verifica che un organizzatore NON possa modificare l'evento di un altro organizzatore"""
        event = Event.objects.create(
            title="Workshop di demo_organizer1",
            description="Descrizione",
            date=self.future_date,
            location="Firenze",
            category=self.category,
            organizer=self.organizer1
        )

        # Effettua il login con demo_organizer2
        self.client.login(username="demo_organizer2", password="password123")
        response = self.client.post(reverse('event_edit', kwargs={'pk': event.id}), {
            'title': 'Tentativo di modifica',
            'description': 'Modificato',
            'date': self.future_date.strftime('%Y-%m-%dT%H:%M'),
            'location': 'Firenze',
            'category': self.category.id
        })
        # Deve reindirizzare con errore
        self.assertEqual(response.status_code, 302)
        event.refresh_from_db()
        self.assertNotEqual(event.title, 'Tentativo di modifica')

    def test_attendee_can_register_to_active_event(self):
        """Verifica che un partecipante possa iscriversi a un evento attivo"""
        event = Event.objects.create(
            title="Seminario AI",
            description="Descrizione",
            date=self.future_date,
            location="Firenze",
            category=self.category,
            organizer=self.organizer1
        )
        self.client.login(username="demo_attendee1", password="password123")
        response = self.client.post(reverse('event_register', kwargs={'pk': event.id}))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Registration.objects.filter(event=event, attendee=self.attendee).exists())

    def test_organizer_cannot_register_to_event(self):
        """Verifica che un organizzatore NON possa iscriversi come partecipante a un evento"""
        event = Event.objects.create(
            title="Seminario AI",
            description="Descrizione",
            date=self.future_date,
            location="Firenze",
            category=self.category,
            organizer=self.organizer1
        )
        self.client.login(username="demo_organizer1", password="password123")
        response = self.client.post(reverse('event_register', kwargs={'pk': event.id}))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Registration.objects.filter(event=event, attendee=self.organizer1).exists())

    def test_cannot_register_to_concluded_event(self):
        """Verifica che non sia possibile iscriversi a eventi conclusi (nel passato)"""
        past_date = timezone.now() - timedelta(days=1)
        event = Event.objects.create(
            title="Evento Storico",
            description="Nel passato",
            date=past_date,
            location="Firenze",
            category=self.category,
            organizer=self.organizer1
        )
        # Sforza l'inserimento nel database bypassando il clean del form per simulare un evento concluso
        Event.objects.filter(id=event.id).update(date=past_date)

        self.client.login(username="demo_attendee1", password="password123")
        response = self.client.post(reverse('event_register', kwargs={'pk': event.id}))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Registration.objects.filter(event=event, attendee=self.attendee).exists())