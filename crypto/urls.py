from django.urls import path
from .apps import APP_NAME
from . import views,apis
app_name=APP_NAME
urlpatterns = [
    path('',views.BasicView().home,name="home"),
    path("crypto_token/<int:pk>/",views.CryptoTokenViews().crypto_token,name="crypto_token"),
    path("crypto_tokens/",views.CryptoTokenViews().crypto_tokens,name="crypto_tokens"),
    path("add_crypto_token/",apis.CryptoTokenApi().add_crypto_token,name="add_crypto_token"),
]
