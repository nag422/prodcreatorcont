from django.urls import path
from django.views.generic import TemplateView
# from django.contrib.auth import views as auth_views
# have to import forms for auth_views
from . import views
app_name="authentication"
urlpatterns = [

    path('signup/', views.account_register, name='register'),
    path('activate/<slug:uidb64>/<slug:token>)/', views.account_activate, name='activate'),

    path('admin/saveuser/',views.saveUser, name="saveuser"),
    path('admin/getsingleuser/',views.getsingleUser, name="getsingleUser"),
    path('admin/deleteusers/',views.deleteUsers, name="deleteUsers"),

    path('admin/userupdate/',views.updateUser, name="updateUser"),

    

    # path('login/', auth_views.LoginView.as_view(template_name='account/registration/login.html',
    #                                             form_class=UserLoginForm), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(next_page='/account/login/'), name='logout'),

    # Reset password

    # path('password_reset/', auth_views.PasswordResetView.as_view(template_name="account/user/password_reset_form.html",
    #                                                              success_url='password_reset_email_confirm',
    #                                                              email_template_name='account/user/password_reset_email.html',
    #                                                              form_class=PwdResetForm), name='pwdreset'),
    # path('password_reset_confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='account/user/password_reset_confirm.html',
    #                                                                                             success_url='password_reset_complete/',
    #                                                                                             form_class=PwdResetConfirmForm),
    #      name="password_reset_confirm"),
    # path('password_reset/password_reset_email_confirm/',
    #      TemplateView.as_view(template_name="account/user/reset_status.html"), name='password_reset_done'),
    # path('password_reset_confirm/Mg/password_reset_complete/',
    #      TemplateView.as_view(template_name="account/user/reset_status.html"), name='password_reset_complete'),

    # FrontEnd Auth
    path('registeruser/', views.authRegisteraccount, name='authRegisteraccount'),
    path('registervalidation/', views.authRegistervalidation, name='authRegistervalidation'),
    path('signinsave/', views.loginView, name='loginView'),
    path('signout/', views.logoutView, name='logoutView'),

    path('aboutme/', views.WhoAmi, name='WhoAmi'),
    path('getuserchip/', views.authChipUserGet, name='authChipUserGet'),
    
    

    
    # Dashboard
    path('profile/edit/', views.edit_details, name='edit_details'),
    path('profile/delete_user/', views.delete_user, name='delete_user'),
    path('profile/delete_confirm/', TemplateView.as_view(template_name="account/user/delete_confirm.html"), name='delete_confirmation'),


]