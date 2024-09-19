from django.contrib import admin
from django.urls import path, include
# from . import views
from django.contrib.auth import views as auth_views
from . import views
from .views import UserLoginView, UserLogoutView , UserProfileView # ..PyQuiz.views
from allauth.account.views import login, logout, LogoutView

urlpatterns = [
    # path('', views.home, name='PyQuiz-home'),
    # path('about/', views.about, name='PyQuiz-about'),
    # path('admin/', admin.site.urls),
    path('users/', include('allauth.urls')),
    path("login/", UserLoginView.as_view(template_name="PyQuiz/login.html"), name="users_login"),
    path("signup/", views.register, name="users_signup"),
    path("logout/", UserLogoutView.as_view(template_name="PyQuiz/logout.html"), name="users_logout"),
    
    path("profile/", views.profile, name="users_profile"),
    # path("profile/", UserProfileView.as_view(template_name="PyQuiz/profile.html"), name="users_profile"),
]


# logout_.html

# logout.html  template_name="PyQuiz/logout.html"