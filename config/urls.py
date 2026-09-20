from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from games.views import SignUpView

urlpatterns = [
    path('', RedirectView.as_view(url='/games/', permanent=True)),
    path('admin/', admin.site.urls),
    path('games/', include('games.urls')),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
]
