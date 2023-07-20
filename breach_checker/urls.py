from django.urls import include, path
from django.contrib import admin
from admin_app import views as admin_views

urlpatterns = [
    # Other URL patterns...
    path('', include('breach_app.urls')),
    path('admin/', admin.site.urls),
    path('adminapp/', include('admin_app.urls', namespace='adminapp')),
    path('adminapp/login/', admin_views.admin_login, name='admin_login'),
    path('adminapp/', admin_views.admin_home, name='admin_home'),
]
