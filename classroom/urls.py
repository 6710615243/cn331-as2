from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# Define a list of URLs patterns
urlpatterns = [
    path('', views.index, name = 'index'),
    path("register/", views.register, name="register"),
    path("reserve/<int:room_id>", views.reserve_room, name="reserve"),
    path("cancel/", views.cancel_reservation, name="cancel"),

    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('admin/', views.login_admin, name='admin')
]