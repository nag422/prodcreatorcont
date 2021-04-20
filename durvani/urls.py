from django.contrib import admin
from django.urls import path,include,re_path
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('quizz.urls',namespace="quizz")),  
    path('durvani/', include('blog.urls',namespace="blog")),  

    path('auth/', include('authentication.urls',namespace='account')),
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.MEDIA_URL,document_root='static/static_cdn/build/'+settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
# urlpatterns += [re_path(r'^.*\/', TemplateView.as_view(template_name='base.html'))] 

admin.site.index_title="ContentBond"
admin.site.site_header="The ContentBond Administration"
admin.site.site_title="ContentBond"