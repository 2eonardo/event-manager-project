"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from events import views as events_views
from users import views as users_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Redirect root to login (no anonymous access)
    path('', users_views.login_view, name='home'),

    # Event URLs
    path('events/', events_views.event_list, name='event_list'),
    path('organizer/<int:organizer_id>/events/', events_views.organizer_events, name='organizer_events'),
    path('events/<int:pk>/', events_views.event_detail, name='event_detail'),
    path('events/create/', events_views.event_create, name='event_create'),
    path('events/<int:pk>/edit/', events_views.event_edit, name='event_edit'),
    path('events/<int:pk>/delete/', events_views.event_delete, name='event_delete'),
    path('events/<int:pk>/register/', events_views.event_register, name='event_register'),
    path('events/<int:pk>/unregister/', events_views.event_unregister, name='event_unregister'),

    # User URLs
    path('login/', users_views.login_view, name='login'),
    path('signup/', users_views.signup_view, name='signup'),
    path('logout/', users_views.logout_view, name='logout'),
    path('profile/', users_views.profile_view, name='profile'),
    path('profile/edit/', users_views.profile_edit_view, name='profile_edit'),
]
