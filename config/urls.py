# config/urls.py
from django.contrib import admin
from django.urls import path
from events import views as events_views
from users import views as users_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Redirect root to login (no anonymous access)
    path('', users_views.login_view, name='home'),

    # Event URLs (Viste funzionali)
    path('events/', events_views.event_list, name='event_list'),
    path('organizer/<int:organizer_id>/events/', events_views.organizer_events, name='organizer_events'),
    path('events/<int:pk>/', events_views.event_detail, name='event_detail'),
    
    # Class-Based Views per creazione, modifica e cancellazione (.as_view())
    path('events/create/', events_views.EventCreateView.as_view(), name='event_create'),
    path('events/<int:pk>/edit/', events_views.EventUpdateView.as_view(), name='event_edit'),
    path('events/<int:pk>/delete/', events_views.EventDeleteView.as_view(), name='event_delete'),
    
    # Iscrizione e disiscrizione
    path('events/<int:pk>/register/', events_views.event_register, name='event_register'),
    path('events/<int:pk>/unregister/', events_views.event_unregister, name='event_unregister'),

    # User URLs
    path('login/', users_views.login_view, name='login'),
    path('signup/', users_views.signup_view, name='signup'),
    path('logout/', users_views.logout_view, name='logout'),
    path('profile/', users_views.profile_view, name='profile'),
    path('profile/edit/', users_views.profile_edit_view, name='profile_edit'),
]