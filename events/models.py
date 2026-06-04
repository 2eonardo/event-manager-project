from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        # Dice a Django Admin di scrivere "Categories" invece di "Categorys" al plurale
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)

    # NUOVO CAMPO: Relazione ForeignKey con la Categoria.
    # Se eliminiamo una categoria, gli eventi ad essa collegati non vengono cancellati (on_delete=models.SET_NULL)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='events'
    )

    # Relazione ForeignKey con l'utente (l'organizzatore dell'evento)
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='organized_events'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # NUOVA IMPOSTAZIONE: Ordina gli eventi dal più vicino (nel tempo) al più lontano
        ordering = ['date']

    def __str__(self):
        return self.title


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