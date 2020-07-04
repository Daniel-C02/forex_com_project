"""forex_community_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf import settings
from community import views
# from django.conf.urls import url
# from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    # Auth
    path('signup/', views.signupuser, name='signupuser'),
    path('login/', views.loginuser, name='loginuser'),
    path('logout/', views.logoutuser, name='logoutuser'),

    # Community
    path('', views.primaryhome, name='primaryhome'),
    path('home/', views.home, name='home'),
    path('profile/', views.userprofile, name='userprofile'),
    path('fullcommunity/', views.fullcommunity, name='fullcommunity'),
    path('feed/', views.feed, name='feed'),
    path('education/', views.education, name='education'),

    #edit/post/change
    path('posttrade/', views.posttrade, name='posttrade'),
    path('edituserprofile/', views.edituserprofile, name='edituserprofile'),
    path('change_password/', views.change_password, name='change_password'),

    #view
    path('trade/<int:trade_pk>/', views.viewyourtrade, name='viewyourtrade'),
    path('usertrade/<int:trade_pk>/<int:user_pk>/', views.viewusertrade, name='viewusertrade'),
    path('userpro/<int:user_pk>/', views.viewuser, name='viewuser'),

    #Delete
    path('alltradeshtml/', views.alltradeshtml, name='alltradeshtml'),
    path('accounthtml/', views.accounthtml, name='accounthtml'),
    path('deletetrade/<int:trade_pk>/', views.deletetrade, name='deletetrade'),
    path('deletealltrades/<int:user_pk>/', views.deletealltrades, name='deletealltrades'),
    path('deleteaccount/<int:user_pk>/', views.deleteaccount, name='deleteaccount'),

    #Braintree Payment
    # path('checkouts/new/', views.new_checkout, name='new_checkout'),
    # path('checkouts/<str:transaction_id>/', views.show_checkout, name='show_checkout'),
    # path('checkouts/', views.create_checkout, name='create_checkout'),

    #PayPal Payment
    path('process-payment/', views.process_payment, name='process_payment'),
    path('payment-done/', views.payment_done, name='payment_done'),
    path('payment-cancelled/', views.payment_canceled, name='payment_cancelled'),

    #Password Reset 
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="community/pswd_reset/reset_pswd.html"), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="community/pswd_reset/pswd_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="community/pswd_reset/pswd_reset_confirm.html"), name='password_reset_confirm'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="community/pswd_reset/pswd_reset_complete.html"), name='password_reset_complete'),
] 
# if os.environ.get('DJANGO_ENV') != 'production':
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)



