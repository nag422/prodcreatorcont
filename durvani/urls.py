from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('quizz.urls',namespace="quizz")),  
    path('durvani/', include('blog.urls',namespace="blog")),  

    path('auth/', include('authentication.urls',namespace='account'))
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)