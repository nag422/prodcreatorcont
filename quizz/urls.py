from django.urls import path
from . import views
from django.views.generic import TemplateView,RedirectView

app_name='quizz'
urlpatterns = [
    path('quiz/',views.quiz,name="quiz"),
    path('profile/',views.profile),
    path('ex1_templateview/',TemplateView.as_view(template_name="1templateview.html",extra_context={'title':'extracontext'})),
    path('ex2_templateview/',views.Ex2View.as_view()),
    path('rdt/', RedirectView.as_view(url='http://youtube.com/veryacademy'), name='go-to-very'),
    path('ex3/<int:pk>/',views.PostPreLoadTaskView.as_view(),name='redirect-task'),
    path('ex4/<int:pk>/',views.SinglePostView.as_view(),name='singlepost'),
    path('listviewex/',views.BookListView.as_view(),name='book-list'),
    path('<slug:slug>/',views.BookDetailView.as_view(),name='book-detail'),
    path('g/<str:genre>/',views.BookListView.as_view(),name='book-detailkwarg'),
    path('g/add/form/', views.AddBookView.as_view(), name='add'),
    path('g/addcreate/form/', views.AddBookViewcreate.as_view(), name='addcreate'),
    path('g/addupdate/form/<slug:pk>', views.AddEditView.as_view(), name='addupdate'),

    path('auth/signin',views.movieplex),
    path('admin/contentrequest/',views.movieplex),

    path('admin/saveproduct/',views.save_product,name='saveproduct'),
    path('admin/requestsaveproduct/',views.requestsaveproduct,name='requestsaveproduct'),
    path('admin/getProductsall/',views.getProductsall,name='getProductsall'),
    # Group
    path('admin/creategroup/',views.createGroup,name='createGroup'),
    path('admin/getallgroups/',views.getAllgroups,name='getAllgroups'),

    # path('admin/getallprodlikes/',views.getProductswithlikes,name='getProductswithlikes'),
    path('admin/addliketoproduct/',views.addliketoproduct,name='addliketoproduct'),
    path('admin/addboughtproduct/',views.addboughtproduct,name='addboughtproduct'),
    path('admin/getproductsallbagged/',views.getProductsallbagged,name='getProductsallbagged'),
    path('admin/getproductsallliked/',views.getProductsallliked,name='getProductsallliked'),


    
]
