from django.urls import path
from appointment import views 
from django.contrib.auth.decorators import login_required , permission_required  

urlpatterns = [
    path("register", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("book-appointment" , login_required(views.search) , name="appointment"),
    path("search-and-book-appointment" , views.BookAppointment.as_view() , name="search"),
    path("logout", views.logout_request, name= "logout"),
]