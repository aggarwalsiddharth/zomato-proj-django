from django.urls import path
from . import views

urlpatterns = [

    path('',views.index,name = 'index'),
    path('accounts/login/',views.login_view,name = 'login'),
    path('accounts/logout/',views.logout_view,name = 'logout'),
    path('signup/',views.Signup.as_view(),name = 'signup'),
    path('addrestaurant/',views.Addrestaurant.as_view(),name='addrestaurant'),
    path('success/',views.SuccessView.as_view(),name = 'success'),
    path('restaurants/',views.RestaurantList.as_view(),name = 'restaurants'),
    path('restaurant/<int:pk>',views.RestaurantDetail.as_view(),name = 'restaurant'),



]