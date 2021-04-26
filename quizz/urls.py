from django.urls import path
from . import views
from django.views.generic import TemplateView,RedirectView

app_name='quizz'
urlpatterns = [
    path('getcsrf/default/',views.get_csrf,name="csrf"),
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
    path('auth/password_reset/',views.movieplex2),
    path('admin/contentrequest/',views.movieplex),

    path('admin/saveproduct/',views.save_product,name='saveproduct'),
    path('admin/saveproductbyadmin/',views.save_product_by_admin,name='saveproductadmin'),
    path('admin/editproductsave/',views.editProductSave,name='editproductsave'),

    path('admin/getadminmesssages/',views.GetAdminMessages,name='getadminmessages'),
    path('admin/getadminmesssagesreply/',views.GetAdminMessagesReply,name='getadminmessagesreply'),
    path('admin/deletemessages/',views.DeleteMessages,name='deletemessages'),

    
    
    path('admin/requestsaveproduct/',views.requestsaveproduct,name='requestsaveproduct'),
    path('admin/getProductsall/',views.getProductsall,name='getProductsall'),
    path('admin/getproductsallbyusers/',views.getProductsallbyUsers,name='getProductsallbyUsers'),

    path('admin/getproductbyid/',views.getProductById,name='getProductById'),


    
    # Group
    path('admin/creategroup/',views.createGroup,name='createGroup'),
    path('admin/getallgroups/',views.getAllgroups,name='getAllgroups'),
    path('admin/deletegroups/',views.deleteGroups,name='deleteGroups'),


    

    path('admin/assignedtogroup/',views.assignedtogroup,name='assignedtogroup'),


    path('admin/getproductchip/', views.getProductChip, name='getProductChip'),
    path('admin/saveproductsforusers/', views.UserProductSave, name='UserProductSave'),
    path('admin/saveproductsforgroups/', views.GroupProductSave, name='GroupProductSave'),

    # path('admin/getallprodlikes/',views.getProductswithlikes,name='getProductswithlikes'),
    path('admin/addliketoproduct/',views.addliketoproduct,name='addliketoproduct'),
    path('admin/addboughtproduct/',views.addboughtproduct,name='addboughtproduct'),
    path('admin/getproductsallbagged/',views.getProductsallbagged,name='getProductsallbagged'),
    path('admin/getproductsallliked/',views.getProductsallliked,name='getProductsallliked'),
    path('admin/productstatus/',views.productstatus,name='productstatus'),

    # Admin Copy paths
    path('admin/getproductsalllikedbyid/',views.getProductsalllikedbyuserid,name='getProductsalllikedbyuserid'),
    path('admin/getproductsallbaggedbyid/',views.getProductsallbaggedbyuserid,name='getProductsallbaggedbyuserid'),
    path('admin/getproductsallbyusersbyid/',views.getProductsallbyUsersbyid,name='getProductsallbyUsersbyid'),
    path('admin/getuploadsallbyusersbyid/',views.getUploadsallbyusersbyid,name='getUploadsallbyusersbyid'),
    


    # Chat

    path('admin/chat/users/',views.MessageChatusers,name='messageChatusers'),
    path('admin/chat/savemessage/',views.MessageChatMessages,name='savemessage'),

    path('admin/getsellermessages/',views.getsellermessages,name='getsellermessages'),
    path('admin/getbuyermessages/',views.getbuyermessages,name='getbuyermessages'),

    path('admin/getnotifications/',views.NotifyGetter,name='NotifyGetter'),


    # Dashboard

    path('admin/dashboardview/',views.dashboardView,name='dashboardview'),
    path('admin/dashboardviewseller/',views.dashboardviewsellerView,name='dashboardviewseller'),
    path('admin/dashboardviewbuyerview/',views.dashboardviewbuyerView,name='dashboardviewbuyerView')

    
    
]
