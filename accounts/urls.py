from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.profile_update_view, name='profile_update'),
    path('orders/', views.orders_view, name='orders'),
    path('password/change/', views.CustomPasswordChangeView.as_view(), name='change_password'),
]