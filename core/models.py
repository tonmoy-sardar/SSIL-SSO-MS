from django.db import models
from django.contrib.auth.models import User
# from PIL import Image
# import os
from dynamic_media import get_directory_path

from django.core.validators import URLValidator

class TCorePermissions(models.Model):
    cp_u = models.IntegerField(default=0, blank=True, null=True)
    cp_g = models.IntegerField(default=0, blank=True, null=True)
    cp_o = models.IntegerField(default=0, blank=True, null=True)
    
    cp_created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='cp_created_by',blank=True,null=True)
    cp_created_at=models.DateTimeField(auto_now_add=True)
    cp_updated_at=models.DateTimeField(auto_now =True)
    cp_updated_by=models.ForeignKey(User, on_delete=models.CASCADE, related_name='cp_updated_by',blank=True,null=True)

    class Meta:
        db_table = 't_core_permissions'
        unique_together = ('cp_u', 'cp_g', 'cp_o')

    def __str__(self):
        return str(self.id)

class TCoreRole(models.Model):
    """ t_core_roles """
    cr_name = models.CharField(max_length=100, blank=True,null=True)
    cr_parent_id = models.IntegerField(default = 0)
    cr_is_deleted = models.BooleanField(default=False)

    cr_created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='cr_created_by',blank=True,null=True)
    cr_created_at=models.DateTimeField(auto_now_add=True)
    cr_updated_at=models.DateTimeField(auto_now =True)
    cr_updated_by=models.ForeignKey(User, on_delete=models.CASCADE, related_name='cr_updated_by',blank=True,null=True)
    cr_deleted_at=models.DateTimeField(auto_now =True)
    cr_deleted_by=models.ForeignKey(User, on_delete=models.CASCADE, related_name='cr_deleted_by',blank=True,null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 't_core_roles'
        # unique_together = ('cr_name', 'cr_parent_id',)

class TCoreModule(models.Model):
    cm_name = models.CharField(max_length=100, blank=True,null=True, unique=True)
    cm_desc = models.TextField(blank=True, null=True)
    cm_icon = models.ImageField(upload_to=get_directory_path, default=None, blank=True, null=True)
    # cm_url = models.TextField(validators=[URLValidator()], blank=True, null=True)
    cm_url = models.TextField(blank=True, null=True)
    cm_permissions = models.ForeignKey(TCorePermissions, on_delete=models.CASCADE, related_name='cm_permissions', blank=True, null=True)
    cm_is_deleted = models.BooleanField(default=False)
    cm_is_editable = models.BooleanField(default=True)

    cm_created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='cm_created_by',blank=True,null=True)
    cm_created_at=models.DateTimeField(auto_now_add=True)
    cm_updated_at=models.DateTimeField(auto_now =True)
    cm_updated_by=models.ForeignKey(User, on_delete=models.CASCADE, related_name='cm_updated_by',blank=True,null=True)
    cm_deleted_at=models.DateTimeField(auto_now =True)
    cm_deleted_by=models.ForeignKey(User, on_delete=models.CASCADE, related_name='cm_deleted_by',blank=True,null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 't_core_modules'


class TCoreFunctionalArea(models.Model):
    cfa_name = models.CharField(max_length=100, blank=True,null=True)
    cfa_parent_id = models.IntegerField(default = 0)
    cfa_is_deleted = models.BooleanField(default=False)

    cfa_created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='cfa_created_by',blank=True,null=True)
    cfa_created_at=models.DateTimeField(auto_now_add=True)
    cfa_updated_at=models.DateTimeField(auto_now =True)
    cfa_updated_by=models.ForeignKey(User, on_delete=models.CASCADE, related_name='cfa_updated_by',blank=True,null=True)
    cfa_deleted_at=models.DateTimeField(auto_now =True)
    cfa_deleted_by=models.ForeignKey(User, on_delete=models.CASCADE, related_name='cfa_deleted_by',blank=True,null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 't_core_functional_area'


class TCoreLogicalAreas(models.Model):
    """ t_core_groups """
    cla_name = models.CharField(max_length=100, blank=True,null=True)
    cla_is_deleted = models.BooleanField(default=False)

    cla_created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='cla_created_by',blank=True,null=True)
    cla_created_at=models.DateTimeField(auto_now_add=True)
    cla_updated_at=models.DateTimeField(auto_now =True)
    cla_updated_by=models.ForeignKey(User, on_delete=models.CASCADE, related_name='cla_updated_by',blank=True,null=True)
    cla_deleted_at=models.DateTimeField(auto_now =True)
    cla_deleted_by=models.ForeignKey(User, on_delete=models.CASCADE, related_name='cla_deleted_by',blank=True,null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 't_core_logical_areas'


class TCoreOther(models.Model):
    cot_name = models.CharField(max_length=100, blank=True,null=True)
    description = models.TextField(blank=True, null=True)
    cot_is_deleted = models.BooleanField(default=False)

    cot_created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='cot_created_by',blank=True,null=True)
    cot_created_at=models.DateTimeField(auto_now_add=True)
    cot_updated_at=models.DateTimeField(auto_now =True)
    cot_updated_by=models.ForeignKey(User, on_delete=models.CASCADE, related_name='cot_updated_by',blank=True,null=True)
    cot_deleted_at=models.DateTimeField(auto_now =True)
    cot_deleted_by=models.ForeignKey(User, on_delete=models.CASCADE, related_name='cot_deleted_by',blank=True,null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 't_core_others'

class TCoreUnit(models.Model):
    c_name = models.CharField(max_length=100, blank=True, null=True)
    c_is_deleted = models.BooleanField(default=False)

    c_created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='c_created_by', blank=True,
                                       null=True)
    c_created_at = models.DateTimeField(auto_now_add=True)
    c_updated_at = models.DateTimeField(auto_now=True)
    c_updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='c_updated_by', blank=True,
                                       null=True)
    c_owned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='c_owned_by', blank=True,
                                       null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 't_core_units'