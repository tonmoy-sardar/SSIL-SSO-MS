from django.db import models
from django.contrib.auth.models import User
from core.models import *
# from users.models import *
# collections 
import collections


class TMasterModuleLogicalAreas(models.Model):
    mmla_logical_areas = models.ForeignKey(TCoreLogicalAreas, on_delete=models.CASCADE,related_name='mmla_logical_areas')
    mmla_module = models.ForeignKey(TCoreModule, on_delete=models.CASCADE,related_name='mmla_module')
    mmla_name = models.CharField(max_length=100, blank=True,null=True)

    class Meta:
        db_table = 't_master_module_logical_areas'

    def __str__(self):
        return str(self.id)
class TMasterModuleFunctionalArea(models.Model):
    mmfa_functional_area = models.ForeignKey(TCoreFunctionalArea, on_delete=models.CASCADE,related_name='mmfa_functional_area')
    mmfa_module = models.ForeignKey(TCoreModule, on_delete=models.CASCADE,related_name='mmfa_module')
    mmfa_name = models.CharField(max_length=100, blank=True,null=True)
    
    class Meta:
        db_table = 't_master_module_functional_area'

    def __str__(self):
        return str(self.id)
class TMasterModuleOther(models.Model):
    mmo_other = models.ForeignKey(TCoreOther, on_delete=models.CASCADE,related_name='mmo_other')
    mmo_module = models.ForeignKey(TCoreModule, on_delete=models.CASCADE,related_name='mmo_module')
    mmo_name = models.CharField(max_length=100, blank=True,null=True)
    parent_id = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='t_m_updated_by', blank=True, null=True)
    class Meta:
        db_table = 't_master_module_other'

    def __str__(self):
        return str(self.id)
class TMasterModuleGroup(models.Model):
    mmg_name = models.CharField(max_length=100, blank=True, null=True)
    mmg_group_code = models.CharField(max_length=18, unique=True)
    mmg_module = models.ForeignKey(TCoreModule, on_delete=models.CASCADE, related_name='mmg_module')

    mmg_is_deleted = models.BooleanField(default=False)
    mmg_created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mmg_created_by', blank=True,
                                      null=True)
    mmg_created_at = models.DateTimeField(auto_now_add=True)
    mmg_updated_at = models.DateTimeField(auto_now=True)
    mmg_updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mmg_updated_by', blank=True,
                                      null=True)
    mmg_deleted_at = models.DateTimeField(auto_now=True)
    mmg_deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mmg_deleted_by', blank=True,
                                      null=True)


    class Meta:
        db_table = 't_master_module_group'

    def __str__(self):
        return str(self.id)
class TMasterModuleRole(models.Model):
    """docstring for ClassName"""
    mmr_module = models.ForeignKey(TCoreModule, on_delete=models.CASCADE,related_name='mmr_module')
    mmr_role = models.ForeignKey(TCoreRole, on_delete=models.CASCADE,related_name='mmr_role')
    mmr_permissions = models.ForeignKey(TCorePermissions, on_delete=models.CASCADE, related_name='mmr_permissions', blank=True,null=True)
    mmr_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mmr_user',blank=True,null=True)
    mmr_group = models.ForeignKey(TMasterModuleGroup, on_delete=models.CASCADE, related_name='mmr_group',blank=True,null=True)
    # mmr_parent_id = models.IntegerField(default = 0)
    class Meta:
        db_table = 't_master_module_role'
        unique_together = ('mmr_module', 'mmr_role','mmr_user')

    def __str__(self):
        return str(self.id)

    # def user_details(self):
    #     user_details_dict = collections.OrderedDict()
    #     user_details_data = TCoreUserDetail.objects.filter(cu_user_id=self.mmr_user_id)
    #     for data in user_details_data:
    #         user_details_dict['cu_super_set'] = data.cu_super_set
    #         user_details_dict['cu_phone_no'] = data.cu_phone_no
    #         user_details_dict['cu_emp_code'] = data.cu_emp_code
    #     return user_details_dict
