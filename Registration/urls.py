from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
app_name = "Registration"
urlpatterns = [
    path('signup/', views.signup, name="SignUp"),
    path('login/',views.loginpage, name="Login"),
    path('',views.intro, name="Introduction"),
]