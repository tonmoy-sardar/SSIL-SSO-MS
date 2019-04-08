from django.db import models
from django.contrib.auth.models import User
from core.models import *
from master.models import *

class TCoreLogicalAreasMeta(models.Model):
    lam_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='lam_user')

    lam_logical_areas = models.ForeignKey(TCoreLogicalAreas, on_delete=models.CASCADE,related_name='lam_logical_areas')

    lam_permissions = models.ForeignKey(TCorePermissions, on_delete=models.CASCADE, related_name='lam_permissions')

    lam_mmla = models.ForeignKey(TMasterModuleLogicalAreas, on_delete=models.CASCADE, related_name='lam_mmla')

    lam_is_deleted = models.BooleanField(default=False)

    lam_created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='lam_created_by',blank=True,null=True)
    lam_created_at=models.DateTimeField(auto_now_add=True)
    lam_updated_at=models.DateTimeField(auto_now =True)
    lam_updated_by=models.ForeignKey(User, on_delete=models.CASCADE, related_name='lam_updated_by',blank=True,null=True)
    lam_deleted_at=models.DateTimeField(auto_now =True)
    lam_deleted_by=models.ForeignKey(User, on_delete=models.CASCADE, related_name='lam_deleted_by',blank=True,null=True)

    class Meta:
        db_table = 't_core_logical_areas_meta'

    def __str__(self):
        return str(self.id)


class TCoreFunctionalAreaMeta(models.Model):
    fam_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='fam_user')

    fam_functional_area = models.ForeignKey(TCoreFunctionalArea, on_delete=models.CASCADE,related_name='fam_functional_area')

    fam_permissions = models.ForeignKey(TCorePermissions, on_delete=models.CASCADE, related_name='fam_permissions')

    fam_mmfa = models.ForeignKey(TMasterModuleFunctionalArea, on_delete=models.CASCADE, related_name='fam_mmfa')

    fam_is_deleted = models.BooleanField(default=False)

    fam_created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='fam_created_by',blank=True,null=True)
    fam_created_at=models.DateTimeField(auto_now_add=True)
    fam_updated_at=models.DateTimeField(auto_now =True)
    fam_updated_by=models.ForeignKey(User, on_delete=models.CASCADE, related_name='fam_updated_by',blank=True,null=True)
    fam_deleted_at=models.DateTimeField(auto_now =True)
    fam_deleted_by=models.ForeignKey(User, on_delete=models.CASCADE, related_name='fam_deleted_by',blank=True,null=True)

    class Meta:
        db_table = 't_core_functional_area_meta'

    def __str__(self):
        return str(self.id)

class TCoreUserMeta(models.Model):
    um_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='um_user')

    um_la_meta = models.ForeignKey(TCoreLogicalAreasMeta, on_delete=models.CASCADE,related_name='um_la_meta')

    um_fa_meta = models.ForeignKey(TCoreFunctionalAreaMeta, on_delete=models.CASCADE,related_name='um_fa_meta')

    um_permissions = models.ForeignKey(TCorePermissions, on_delete=models.CASCADE, related_name='um_permissions')

    um_other = models.ForeignKey(TCoreOther, on_delete=models.CASCADE, related_name='um_other')

    um_mmo = models.ForeignKey(TMasterModuleOther, on_delete=models.CASCADE, related_name='um_mmo')

    um_mmr = models.ForeignKey(TMasterModuleRole, on_delete=models.CASCADE, related_name='um_mmr', blank=True,null=True)

    um_module = models.ForeignKey(TCoreModule, on_delete=models.CASCADE, related_name='um_role')

    um_is_deleted = models.BooleanField(default=False)

    um_created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='um_created_by',blank=True,null=True)
    um_created_at=models.DateTimeField(auto_now_add=True)
    um_updated_at=models.DateTimeField(auto_now =True)
    um_updated_by=models.ForeignKey(User, on_delete=models.CASCADE, related_name='um_updated_by',blank=True,null=True)
    um_deleted_at=models.DateTimeField(auto_now =True)
    um_deleted_by=models.ForeignKey(User, on_delete=models.CASCADE, related_name='um_deleted_by',blank=True,null=True)

    class Meta:
        db_table = 't_core_user_meta'

    def __str__(self):
        return str(self.id)