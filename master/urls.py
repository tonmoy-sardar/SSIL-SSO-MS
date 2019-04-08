from master import views
from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path

from rest_framework.authtoken import views as rest_framework_views

urlpatterns = [
    path('user-module-role_list/', views.UserModuleRoleListCreate.as_view()),
    path('module-role_create/', views.ModuleRoleCreate.as_view()),
    path('module-role_relation-mapping/<mmr_module_id>/', views.ModuleRoleRelationMapping.as_view()),
    path('free_role-module_list/<mmr_module_id>/', views.FreeModuleRoleList.as_view()),

    path('user_list_by_module_id/<mmr_module_id>/', views.UserList.as_view()),
    path('clone_module-roles/<clone_from>/<clone_to>/', views.CloneModuleRole.as_view()),

    path('module_group_add/', views.TMasterModuleGroupCreateView.as_view()),
    path('t_master_module_group_edit/<pk>/', views.TMasterModuleGroupEditView.as_view()),
    path('t_master_module_group_delete/<pk>/', views.TMasterModuleGroupDeleteView.as_view()),
]