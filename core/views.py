from django.shortcuts import render
from rest_framework import generics
# from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework.authtoken.models import Token
# from django.contrib.auth.models import Permission
# from django.contrib.auth.models import *
from core.serializers import *
from rest_framework.response import Response
from rest_framework import filters
# permission checking
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
#get_current_site
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from pagination import CSLimitOffestpagination,CSPageNumberPagination

class PermissionsListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    # pagination_class =CSPageNumberPagination
    queryset =TCorePermissions.objects.all()
    serializer_class = TCorePermissionsSerializer
    filter_backends = (filters.SearchFilter,)
    def get_queryset(self):
        queryset = TCorePermissions.objects.all()
        cp_u = self.request.query_params.get('cp_u', None)
        cp_g = self.request.query_params.get('cp_g', None)
        cp_o = self.request.query_params.get('cp_o', None)
        print("cp_u: {}, cp_g: {}, cp_o: {}".format(cp_u, cp_g, cp_o))

        if cp_u and cp_g and cp_o:
            queryset = TCorePermissions.objects.filter(cp_u = cp_u, cp_g = cp_g, cp_o = cp_o)
        return queryset
class ModuleListCreate(generics.ListCreateAPIView):
    """docstring for ClassName"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset =TCoreModule.objects.filter(cm_is_deleted=False)
    serializer_class = TCoreModuleSerializer



    # def list(self, request, *args, **kwargs):
    #     response = super(ModuleListCreate, self).list(request, args, kwargs)
    #     response_dict = response.data
    #     for data in response_dict:
    #         data['cm_icon'] = "http://"+get_current_site(request).domain+ settings.MEDIA_URL + data['cm_icon']
    #         print(data['cm_icon'])
    #     print("response_dict: ", type(response_dict))
    #     return response
class ModuleList(generics.ListAPIView):
    """docstring for ClassName"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset =TCoreModule.objects.all()
    serializer_class = TCoreModuleListSerializer

    # def list(self, request, *args, **kwargs):
    #     response = super(ModuleListCreate, self).list(request, args, kwargs)
    #     response_dict = response.data
    #     for data in response_dict:
    #         data['cm_icon'] = "http://"+get_current_site(request).domain+ settings.MEDIA_URL + data['cm_icon']
    #         print(data['cm_icon'])
    #     print("response_dict: ", type(response_dict))
    #     return response
class EditModuleById(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = TCoreModule.objects.all()
    serializer_class =TCoreModuleSerializer
class RoleListCreate(generics.ListCreateAPIView):
    """docstring for ClassName"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = TCoreRole.objects.all()
    serializer_class =TCoreRoleSerializer
class RoleRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """docstring for ClassName"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = TCoreRole.objects.all()
    serializer_class =TCoreRoleSerializer
class UnitAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = TCoreUnit.objects.all()
    serializer_class=UnitAddSerializer

#:::::::::::::::: OBJECTS :::::::::::::#
class OtherAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = TCoreOther.objects.all()
    serializer_class=OtherAddSerializer
class OtherListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = CSPageNumberPagination
    queryset = TMasterModuleOther.objects.all()
    serializer_class=OtherListSerializer
    def get_queryset(self):
        module_id = self.kwargs['module_id']
        #parent_id = self.kwargs['parent_id']
        return TMasterModuleOther.objects.filter(mmo_module=module_id,parent_id=0)
    def list(self, request, *args, **kwargs):
        response = super(OtherListView, self).list(request, args, kwargs)
        #print('data',response.data['results'])
        for data in response.data['results']:
            OtherDetails = TCoreOther.objects.filter(
                pk=data['mmo_other'], cot_is_deleted=False)
            #print('OtherDetails query',OtherDetails.query)
            for e_OtherModuleDetails in OtherDetails:
                #print('OtherDetails',OtherDetails)
                data['cot_name'] = e_OtherModuleDetails.cot_name
                data['description'] = e_OtherModuleDetails.description
                data['cot_is_deleted'] = e_OtherModuleDetails.cot_is_deleted
                data['created_by'] = e_OtherModuleDetails.cot_created_by.username
        return response
class OtherListByParentView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = CSPageNumberPagination
    queryset = TMasterModuleOther.objects.all()
    serializer_class=OtherListSerializer
    def get_queryset(self):
        module_id = self.kwargs['module_id']
        parent_id = self.kwargs['parent_id']
        return TMasterModuleOther.objects.filter(mmo_module=module_id,parent_id=parent_id)
    def list(self, request, *args, **kwargs):
        response = super(OtherListByParentView, self).list(request, args, kwargs)
        parent_id = self.kwargs['parent_id']
        #print('data',response.data['results'])
        response.data['parent_name'] = TCoreOther.objects.only('cot_name').get(pk=parent_id).cot_name
        for data in response.data['results']:
            OtherDetails = TCoreOther.objects.filter(
                pk=data['mmo_other'], cot_is_deleted=False)
            #print('otherDetails', OtherDetails.query)
            if OtherDetails:
                for e_OtherModuleDetails in OtherDetails:
                    print('e_OtherModuleDetails', e_OtherModuleDetails)
                    data['cot_name'] = e_OtherModuleDetails.cot_name
                    data['description'] = e_OtherModuleDetails.description
                    data['cot_is_deleted'] = e_OtherModuleDetails.cot_is_deleted
                    data['created_by'] = e_OtherModuleDetails.cot_created_by.username
        return response
class OtherEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = TCoreOther.objects.all()
    serializer_class=OtherEditSerializer
class OtherDeleteView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = TCoreOther.objects.all()
    serializer_class=OtherDeleteSerializer