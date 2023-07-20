from django.urls import path
from . import views
from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'admin_app'

urlpatterns = [
    path('users/', views.user_list_view, name='user_list'),
    path('redeem-codes/', views.redeemcode_list_view, name='redeem_code_list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    path('users/<int:pk>/edit/', views.UserUpdateView.as_view(), name='user_edit'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),    
    path('redeem-codeadd/', views.RedeemCodeadd, name='redeem_code_add'),
    path('redeem-codes/<int:pk>/edit/', views.RedeemCodeUpdateView.as_view(), name='redeem_code_edit'),
    path('redeem-codes/<int:pk>/delete/', views.RedeemCodeDeleteView.as_view(), name='redeem_code_delete'),
    path('generate/', views.generate_redeem_codes, name='generate_codes'),
    path('login/', views.admin_login, name='admin_login'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('', views.admin_home, name='adminapp'),
]
