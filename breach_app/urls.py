from django.urls import path
from . import views

urlpatterns = [
    path('', views.indexx, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('redeem/', views.redeem_code, name='redeem'),
    path('about/', views.aboutus, name='about'),
]
