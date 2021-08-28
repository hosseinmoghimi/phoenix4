
from phoenix.server_settings import HOME_APP_URLS
from django.contrib import admin
from django.urls import path,include

from .settings import MEDIA_URL, MEDIA_ROOT, STATIC_URL, STATIC_ROOT, DEBUG
from django.views.static import serve
from django.conf.urls import url
# from authentication.views import AuthenticationView

urlpatterns = [
    path('market/', include('market.urls')),
    path('bms/', include('bms.urls')),
    path('projectmanager/', include('projectmanager.urls')),
    # path('accounts/login/', AuthenticationView().login),
    # path('projectmanager/', include('projectmanager.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('farm/', include('farm.urls')),
    path('mafia/', include('mafia.urls')),
    path('core/', include('core.urls')),
    path('calendar/',include('todocalendar.urls')),
    path('help/', include('help.urls')),
    path('web/', include('web.urls')),
    path('accounts/', include('authentication.urls')),
    path('resume/', include('resume.urls')),
    path('messenger/', include('messenger.urls')),
    path('accounting/', include('accounting.urls')),
    path('', include(HOME_APP_URLS)),
    path('stock/', include('stock.urls')),
    path('realestate/', include('realestate.urls')),
    path('forums/', include('phoenix_forums.urls')),
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')),
    # url(r"^forums/", include("pinax.forums.urls", namespace="pinax_forums")),

    url(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
    url('favicon.ico/', serve, {'document_root': STATIC_ROOT}),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),

    url('favicon.ico', serve, {'document_root': MEDIA_ROOT}),
]


SERVER_ON_HEROKU = False
if SERVER_ON_HEROKU:
    from django.conf.urls.static import static
    urlpatterns = urlpatterns+static(STATIC_URL, document_root=STATIC_ROOT)

