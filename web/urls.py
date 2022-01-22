from . import views,apis
from .apps import APP_NAME
from django.urls import path


app_name=APP_NAME
urlpatterns = [
    path("",views.BasicViews().home,name="home"),
    path('add_contact_message/',apis.BasicApi().add_contact_message,name='add_contact_message'),   
    path("resume_category/<int:pk>/",views.ResumeViews().resume_category,name="resumecategory"),
    path("blogs/",views.BlogViews().blogs,name="blogs"),
    path("feature/<int:pk>/",views.FeatureViews().feature,name="feature"),
    path("blog/<int:pk>/",views.BlogViews().blog,name="blog"),
    path("crypto-token/<int:pk>/",views.CryptoTokenViews().crypto_token,name="cryptotoken"),
    path("ourwork/<int:pk>/",views.OurWorkViews().ourwork,name="ourwork"),
    path("ourteam/<int:pk>/",views.OurTeamViews().ourteam,name="ourteam"),
    path("ourworks/",views.BasicViews().home,name="ourworks"),
    path("about/",views.BasicViews().home,name="about"),
    path("contact/",views.BasicViews().contact,name="contact"),
    path("search/",views.BasicViews().search,name="search"),


    path("add_blog/",apis.BasicApi().add_blog,name="add_blog"),
]
