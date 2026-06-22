from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='events'
    )
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='organized_events'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']

    # --- LOGICA DI CONVALIDA INTEGRATA NEL MODELLO (FAT MODEL) ---
    def clean(self):
        super().clean()

        # 1. Controlla la validità della data (deve essere nel futuro)
        if self.date:
            is_new = not self.pk
            date_changed = False

            # Se l'evento esiste già, controlliamo se la data è stata effettivamente modificata
            if not is_new:
                old_event = Event.objects.filter(pk=self.pk).first()
                if old_event and old_event.date != self.date:
                    date_changed = True

            # Blocca le date passate sia alla creazione sia alla modifica della data
            if (is_new or date_changed) and self.date < timezone.now():
                raise ValidationError("La data dell'evento deve essere nel futuro.")

        # 2. Impedisci la creazione di eventi duplicati dallo stesso organizzatore
        if hasattr(self, 'organizer') and self.organizer:
            duplicati = Event.objects.filter(
                title__iexact=self.title,
                date=self.date,
                location__iexact=self.location,
                organizer=self.organizer
            )
            if self.pk:
                duplicati = duplicati.exclude(pk=self.pk)
            if duplicati.exists():
                raise ValidationError("Hai già creato un evento identico (stesso titolo, data e luogo).")


class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    attendee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='registrations'
    )
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'attendee')

    def __str__(self):
        return f"{self.attendee.username} -> {self.event.title}"