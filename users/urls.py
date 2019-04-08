from users import views
from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path

from rest_framework.authtoken import views as rest_framework_views

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('login/', views.LoginAuthToken.as_view()),
    path('add_user/',views.UsersSignInListCreate.as_view()),
    path('edit_user/<pk>/',views.UsersSignInListCreate.as_view()),
    path('change_password/',views.ChangePasswordView.as_view()),
    path('forgot_password/',views.ForgotPasswordView.as_view()),
    path('logout/',views.Logout.as_view()),
    path('user_lock_unlock/<pk>/',views.ActiveInactiveUserView.as_view()),
    path('user_edit/<cu_user_id>/',views.EditUserView.as_view()),

    path('user_module_list/', views.ModuleUserList.as_view()),
]