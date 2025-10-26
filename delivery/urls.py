from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('cart/', views.view_cart, name='view_cart'),  # Add view_cart if you have it, or remove
    path('restaurant/<int:rest_id>/', views.restaurant_menu, name='restaurant_menu'),
    path('restaurant/<int:rest_id>/order/', views.place_order, name='place_order'),
    path('restaurant/<int:rest_id>/payment/', views.payment, name='payment'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # Add other URL patterns if you have the corresponding views
]
