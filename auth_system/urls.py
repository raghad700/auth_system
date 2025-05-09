from django.contrib import admin
from django.urls import path
from accounts.views import RegisterView, LoginView, ProfileView

# Define the URL patterns for the application
urlpatterns = [
    # Django admin interface URL
    path('admin/', admin.site.urls),
    
    # User registration endpoint
    path(
        'api/register/', 
        RegisterView.as_view(),  # Connects to RegisterView class
        name='register'  # Named URL for reverse lookups
    ),
    
    # User authentication endpoint
    path(
        'api/login/', 
        LoginView.as_view(),  # Connects to LoginView class
        name='login'  # Named URL for reverse lookups
    ),
    
    # User profile endpoint (protected)
    path(
        'api/profile/', 
        ProfileView.as_view(),  # Connects to ProfileView class
        name='profile'  # Named URL for reverse lookups
    ),
]