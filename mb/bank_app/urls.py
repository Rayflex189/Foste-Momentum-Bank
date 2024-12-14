from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.verify, name='verify'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('blog/', views.blog, name='blog'),
    path('client/', views.client, name='client'),
    path('contact/', views.contact, name='contact'),
    path('services/', views.services, name='services'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('LoginPage/', views.LoginPage, name='LoginPage'),
    path('profile_setting/', views.profile_setting, name='profile_setting'),
    path('aml/', views.aml, name='aml'),
    path('tac/', views.tac, name='tac'),
    path('imf/', views.imf, name='imf'),
    path('linking_page/', views.linking_view, name='linking_view'),
    path('kyc/', views.kyc, name='kyc'),
    path('statistics/', views.statistics, name='statistics'),
    path('transaction_details/', views.transaction_details, name='transaction_details'),
    path('pending/', views.pending, name='pending'),
    path('loans/', views.loans, name='loans'),
    path('Upgrade_Account/', views.Upgrade_Account, name='Upgrade_Account'),
    path('reset_setting/', views.reset_setting, name='reset_setting'),
    path('logout/', views.LogOut, name='logout'),

    path('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),

    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
