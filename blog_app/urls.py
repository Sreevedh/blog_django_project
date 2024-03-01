from django.urls import path
from .views import signin, home, profile, post_create, update_post,logout_view, signup, post_delete, update_profile_pic

app_name = 'blog_app'

urlpatterns = [
    path('',signin, name='signin'),
    path('home',home, name='home'),
    path('profile/<int:pk>',profile, name='profile'),
    path('create_post',post_create, name='create_post'),
    path('update_post/<int:pk>',update_post, name='update_post'),
    path('logout/',logout_view, name='logout'),
    path('signup/',signup, name='signup'),
    path('delete_post/<int:pk>',post_delete, name='delete_post'),
    path('update_profile_pic',update_profile_pic, name='update_profile_pic'),
]