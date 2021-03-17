from django.urls import path
from . import views
from django.views.generic import TemplateView,RedirectView

app_name='blog'
urlpatterns = [
    path('blog/',views.blog,name="blog"),
    


    
]
