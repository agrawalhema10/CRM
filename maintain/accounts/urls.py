from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('register/',views.RegisterPage,name="register"),
    path('login/',views.LoginPage,name='login'),
    path('logout/',views.logoutUser,name='logout'),
    path('user/',views.userPage,name='user'),
    path('products/',views.products,name='products'),
    path('customer/<str:pk_test>/',views.customers,name='customer'),
    path('createOrder/<str:pk>/',views.createOrder,name="createOrder"),
    path('updateOrder/<str:pk>/',views.update,name='updateOrder'),
    path('deleteOrder/<str:pk>/',views.delete,name='deleteOrder'),
    path('setting/',views.setting,name='setting')
    ]