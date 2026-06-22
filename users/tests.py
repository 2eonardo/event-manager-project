from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from events.models import Event, Category, Registration

User = get_user_model()


class UserAuthenticationAndProfileTests(TestCase):
    def setUp(self):
        self.signup_url = reverse('signup')
        self.login_url = reverse('login')
        self.profile_url = reverse('profile')
        self.profile_edit_url = reverse('profile_edit')

        # Utente demo partecipante (Attendee)
        self.attendee = User.objects.create_user(
            username="demo_attendee1",
            email="attendee1@test.com",
            password="password123",
            role="attendee"
        )

        # Utente demo organizzatore (Organizer)
        self.organizer = User.objects.create_user(
            username="demo_organizer1",
            email="organizer1@test.com",
            password="password123",
            role="organizer"
        )

        self.category = Category.objects.create(name="Tech")
        self.future_date = timezone.now() + timedelta(days=5)

    def test_signup_successful(self):
        response = self.client.post(self.signup_url, {
            'username': 'nuovo_utente_test',
            'email': 'nuovoutente@test.com',
            'first_name': 'Leonardo',
            'last_name': 'Soldani',
            'password1': 'Leonardo7139732!',
            'password2': 'Leonardo7139732!',
            'role': 'attendee'
        })
        self.assertEqual(response.status_code, 302)  # Reindirizzamento riuscito alla bacheca
        self.assertTrue(User.objects.filter(username='nuovo_utente_test').exists())

    def test_prevent_duplicate_email_on_signup(self):
        response = self.client.post(self.signup_url, {
            'username': 'altro_utente',
            'email': 'attendee1@test.com',  # Email già associata a demo_attendee1
            'first_name': 'Nessuno',
            'last_name': 'Nessuno',
            'password1': 'cpx12345!',
            'password2': 'cpx12345!',
            'role': 'attendee'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='altro_utente').exists())

    def test_profile_views_based_on_role_organizer(self):
        event = Event.objects.create(
            title="Conferenza Organizzatore",
            description="Descrizione",
            date=self.future_date,
            location="Firenze",
            category=self.category,
            organizer=self.organizer
        )
        self.client.login(username="demo_organizer1", password="password123")
        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Conferenza Organizzatore")

    def test_profile_views_based_on_role_attendee(self):
        event = Event.objects.create(
            title="Incontro Culturale",
            description="Descrizione",
            date=self.future_date,
            location="Firenze",
            category=self.category,
            organizer=self.organizer
        )
        Registration.objects.create(event=event, attendee=self.attendee)

        self.client.login(username="demo_attendee1", password="password123")
        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Incontro Culturale")

    def test_profile_edit_successful(self):
        self.client.login(username="demo_attendee1", password="password123")
        response = self.client.post(self.profile_edit_url, {
            'first_name': 'Leonardo',
            'last_name': 'Soldani',
            'email': 'soldani.aggiornato@test.com',
            'bio': 'Nuova bio di Leonardo.'
        })
        self.assertEqual(response.status_code, 302)
        self.attendee.refresh_from_db()
        self.assertEqual(self.attendee.email, 'soldani.aggiornato@test.com')
        self.assertEqual(self.attendee.bio, 'Nuova bio di Leonardo.')

    def test_prevent_email_duplication_on_profile_edit(self):
        self.client.login(username="demo_attendee1", password="password123")
        response = self.client.post(self.profile_edit_url, {
            'first_name': 'Leonardo',
            'last_name': 'Soldani',
            'email': 'organizer1@test.com'  # Email dell'organizzatore
        })
        self.assertEqual(response.status_code, 200)  # Ritorna con errore nel form
        self.attendee.refresh_from_db()
        self.assertNotEqual(self.attendee.email, 'organizer1@test.com')

    def test_login_with_email_successful(self):
        response = self.client.post(self.login_url, {
            'username': 'attendee1@test.com',
            'password': 'password123'
        })

        self.assertEqual(response.status_code, 302)

        self.assertTrue('_auth_user_id' in self.client.session)