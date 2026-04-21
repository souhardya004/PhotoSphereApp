from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [

    path('login/', auth_views.LoginView.as_view(template_name='PhotoApp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),

    path('', views.dashboard, name='dashboard'),
    path('photos/', views.all_photos, name='all_photos'),
    path('profile/', views.profile_view, name='profile'),
    path('add/', views.add_photo, name='add_photo'),
    path('edit/<int:id>/', views.edit_photo, name='edit_photo'),
    path('delete/<int:id>/', views.delete_photo, name='delete_photo'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('like/<int:photo_id>/', views.toggle_like, name='toggle_like'),
    path('comment/<int:photo_id>/', views.add_comment, name='add_comment'),
]