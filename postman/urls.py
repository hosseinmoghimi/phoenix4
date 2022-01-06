from .apps import APP_NAME
from . import views,apis
from django.urls import path



app_name=APP_NAME
urlpatterns = [
    path("",views.BasicView().home,name="home"),
    path("letter/<int:pk>/",views.LetterViews().letter,name="letter"),
    path("letters/",views.LetterViews().letters,name="letters"),
    path("add_letter/",apis.LetterApi().add_letter,name="add_letter"),
]
