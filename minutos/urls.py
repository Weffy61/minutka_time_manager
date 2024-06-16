from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView

from django.urls import path, include

from apps.core.views import get_frontpage, get_privacy, get_terms, get_plans, signup


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', get_frontpage, name='frontpage'),
    path('privacy/', get_privacy, name='privacy'),
    path('terms/', get_terms, name='terms'),
    path('plans/', get_plans, name='plans'),
    path('signup/', signup, name='signup'),
    path('login/', LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', include('apps.dashboard.urls'))

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
