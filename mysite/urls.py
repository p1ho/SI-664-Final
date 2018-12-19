from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.urls import path, include

urlpatterns = [
    path('', lambda r: HttpResponseRedirect('meteorite_landings/')),
    path('admin/', admin.site.urls),
    path('auth/', include('social_django.urls', namespace='social')),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL},
         name='logout'),
    path('meteorite_landings/', include('meteorite_landings.urls')),
    path('meteorite_landings/api/rest-auth/registration/', include('rest_auth.registration.urls')),
    # rest-auth path
    path('meteorite_landings/api/rest-auth/', include('rest_auth.urls')),

    path('api-auth/', include('rest_framework.urls')),
    path('meteorite_landings/api/', include('api.urls')),
    path('meteorite_landings/api/rest-auth/', include('rest_auth.urls')),
    path('meteorite_landings/api/rest-auth/registration/', include('rest_auth.registration.urls'))

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
