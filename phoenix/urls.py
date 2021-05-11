
from django.contrib import admin
from django.urls import path,include

from .settings import MEDIA_URL, MEDIA_ROOT, STATIC_URL, STATIC_ROOT, DEBUG
from django.views.static import serve
from django.conf.urls import url
# from authentication.views import AuthenticationView

urlpatterns = [
    # path('accounts/login/', AuthenticationView().login),
    # path('', include('web.urls')),
    path('admin/', admin.site.urls),
    # path('authentication/', include('authentication.urls')),

    url(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
    url('favicon.ico/', serve, {'document_root': STATIC_ROOT}),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),

    url('favicon.ico', serve, {'document_root': MEDIA_ROOT}),
]


SERVER_ON_HEROKU = False
if SERVER_ON_HEROKU:
    from django.conf.urls.static import static
    urlpatterns = urlpatterns+static(STATIC_URL, document_root=STATIC_ROOT)

