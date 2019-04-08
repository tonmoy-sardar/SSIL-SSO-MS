from django.db import models
from django.contrib.auth.models import User
from dynamic_media import get_directory_path
from master.models import *

from PIL import Image
import collections

class TCoreUserDetail(models.Model):
    TYPE_CHOICE = (
        (0,'0'),
        (1,'1'),
        )
    SUPER_SET_CHOICE = (
        ('u','user'),
        ('g','group'),
        ('o','other'),)

    cu_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cu_user')
    # cu_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cu_user')
    cu_type = models.IntegerField(default = 0, choices = TYPE_CHOICE)
    cu_super_set = models.CharField(max_length = 1, choices = SUPER_SET_CHOICE)
    cu_phone_no = models.CharField(max_length = 10, blank=True,null=True, unique=True)
    cu_alt_phone_no = models.CharField(max_length = 10, blank=True,null=True)
    cu_emp_code = models.CharField(max_length = 10, blank=True, null=True)
    cu_profile_img = models.ImageField(upload_to=get_directory_path, default=None)
    cu_dob = models.DateField(max_length=8, default=None, blank=True,null=True)
    cu_is_deleted = models.BooleanField(default=True)

    cu_created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='cu_created_by',blank=True,null=True)
    cu_created_at=models.DateTimeField(auto_now_add=True)
    cu_updated_at=models.DateTimeField(auto_now =True)
    cu_updated_by=models.ForeignKey(User, on_delete=models.CASCADE, related_name='cu_updated_by',blank=True,null=True)
    cu_deleted_at=models.DateTimeField(auto_now =True)
    cu_deleted_by=models.ForeignKey(User, on_delete=models.CASCADE, related_name='cu_deleted_by',blank=True,null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 't_core_user_details'
        unique_together = ('cu_emp_code', 'cu_phone_no',)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        try:
            if self.id is not None:
                previous = TCoreUserDetail.objects.get(id=self.id)
                super(TCoreUserDetail, self).save(force_insert, force_update)
                size = (256, 256)
                if self.cu_profile_img and self.cu_profile_img != previous.cu_profile_img:
                    print('self.cu_profile_img:', self.cu_profile_img)
                    cu_profile_img = Image.open(self.cu_profile_img.path)
                    print("cu_profile_img size:", cu_profile_img.size)
                    cu_profile_img.thumbnail(size, Image.ANTIALIAS)
                    print("logo 2size:", cu_profile_img.size)
                    cu_profile_img.save(self.cu_profile_img.path)
            else:
                super(TCoreUserDetail, self).save(force_insert, force_update)

        except Exception as e:
            raise e
    def applications(self):
        app_list = []
        try:
            mmr_detalis = TMasterModuleRole.objects.filter(mmr_user_id = self.cu_user_id)
            # print("mmr_detalis: ", self.cu_user_id)
            for mmr_data in mmr_detalis:
                mmr_odict = collections.OrderedDict()
                mmr_odict['mmr_module'] = {"id":mmr_data.mmr_module.id,
                                           "cm_name":mmr_data.mmr_module.cm_name}

                mmr_odict['mmr_role'] = {
                                        # "id": mmr_data.mmr_role.id,
                                        "cr_name": mmr_data.mmr_role.cr_name,
                                         # "cr_parent_id": mmr_data.mmr_role.cr_parent_id
                                         }

                mmr_odict['mmr_permissions'] = {"id": mmr_data.mmr_permissions.id,
                                         "cp_u": mmr_data.mmr_permissions.cp_u,
                                         "cp_g": mmr_data.mmr_permissions.cp_g,
                                         "cp_o": mmr_data.mmr_permissions.cp_o
                                         }
                app_list.append(mmr_odict)
            # print("app_list: ", app_list)
            return app_list
        except Exception as e:
            raise e
        # finally:
        #     return app_list


    
