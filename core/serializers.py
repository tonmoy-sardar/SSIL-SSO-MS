from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from core.models import *
from django.contrib.auth.models import *
from rest_framework.exceptions import APIException
from django.conf import settings
# from rest_framework.validators import *
from drf_extra_fields.fields import Base64ImageField # for image base 64
from django.db import transaction, IntegrityError
from master.models import TMasterModuleOther

class TCorePermissionsSerializer(serializers.ModelSerializer):
    cp_created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = TCorePermissions
        fields = ('id','cp_u','cp_g', 'cp_o','cp_created_by')

    # def create(self, validated_data):
    #     permissions = super(TCorePermissionsSerializer, self).create(validated_data)
    #     permissions.save()
    #     return permissions
class TCoreModuleSerializer(serializers.ModelSerializer):
    """docstring for ClassName"""
    # cm_icon = Base64ImageField()
    cm_created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # cm_name = serializers.CharField(required=True)
    # cm_url = serializers.CharField(required=True)
    class Meta:
        model = TCoreModule
        fields = ('id','cm_name', 'cm_icon','cm_desc','cm_url','cm_permissions', 'cm_created_by', 'cm_is_editable')
class TCoreModuleListSerializer(serializers.ModelSerializer):
    """docstring for ClassName"""
    # cm_icon = Base64ImageField()    
    cm_permissions = TCorePermissionsSerializer()
    class Meta:
        model = TCoreModule
        fields = ('id','cm_name', 'cm_icon','cm_desc','cm_url','cm_permissions')
class TCoreRoleSerializer(serializers.ModelSerializer):
    """docstring for ClassName"""
    cr_created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = TCoreRole
        fields = ('id','cr_name', 'cr_parent_id', 'cr_created_by')
class UnitAddSerializer(serializers.ModelSerializer):
    c_created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    c_owned_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = TCoreUnit
        fields = ('id', 'c_name', 'c_created_by', 'c_owned_by')
#:::::::::::::::: OBJECTS :::::::::::::#
class OtherAddSerializer(serializers.ModelSerializer):
    cot_created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    parent_id = serializers.IntegerField(required=False)
    mmo_module = serializers.CharField(required=False)
    class Meta:
        model = TCoreOther
        fields = ('id','cot_name','description','parent_id','cot_created_by','mmo_module')
    def create(self, validated_data):
        try:
            cot_created_by = validated_data.get('cot_created_by')
            parent_id = validated_data.pop('parent_id') if 'parent_id' in validated_data else 0
            with transaction.atomic():
                cot_save_id = TCoreOther.objects.create(
                    cot_name=validated_data.get('cot_name'),
                    description=validated_data.get('description'),
                    cot_created_by=cot_created_by,
                )
                master_module = TMasterModuleOther.objects.create(
                    mmo_other = cot_save_id,
                    mmo_module_id = validated_data.get('mmo_module'),
                    parent_id = parent_id
                )
                response = {
                    'id': cot_save_id.id,
                    'cot_name': cot_save_id.cot_name,
                    'description': cot_save_id.description,
                    'mmo_module':master_module.mmo_module,
                    'parent_id':master_module.parent_id
                }
                return response
        except Exception as e:
            raise e
class OtherListSerializer(serializers.ModelSerializer):
    parent_name = serializers.CharField(required=False)
    class Meta:
        model = TMasterModuleOther
        fields = ('id','mmo_other','mmo_module','parent_id','is_deleted','parent_name')
class OtherEditSerializer(serializers.ModelSerializer):
    cot_updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    parent_id = serializers.IntegerField(required=False)
    mmo_module = serializers.CharField(required=False)
    class Meta:
        model = TCoreOther
        fields = ('id', 'cot_name', 'description', 'parent_id', 'cot_updated_by', 'mmo_module')

    def update(self, instance, validated_data):
        try:
            print('validated_data',validated_data)
            cot_updated_by = validated_data.get('cot_updated_by')
            parent_id = validated_data.pop('parent_id') if 'parent_id' in validated_data else 0
            with transaction.atomic():
                instance.cot_name = validated_data.get('cot_name')
                instance.description = validated_data.get('description')
                instance.cot_updated_by = cot_updated_by
                instance.save()

                TMasterModuleOther.objects.filter(mmo_other=instance.id).delete()
                master_module = TMasterModuleOther.objects.create(
                    mmo_other = instance,
                    mmo_module_id = validated_data.get('mmo_module'),
                    parent_id = parent_id
                )
                response = {
                    'id': instance.id,
                    'cot_name': instance.cot_name,
                    'description': instance.description,
                    'mmo_module':master_module.mmo_module,
                    'parent_id':master_module.parent_id
                }
                return response
        except Exception as e:
            raise e
class OtherDeleteSerializer(serializers.ModelSerializer):
    cot_updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault(),required=False)
    parent_id = serializers.IntegerField(required=False)
    mmo_module = serializers.CharField(required=False)
    is_deleted = serializers.CharField(required=False)
    class Meta:
        model = TCoreOther
        fields = ('id', 'cot_name', 'description', 'parent_id', 'cot_updated_by',
                  'mmo_module','updated_by','is_deleted')

    def update(self, instance, validated_data):
        try:
            cot_updated_by = validated_data.get('cot_updated_by')
            updated_by = validated_data.get('updated_by')
            instance.cot_is_deleted = True
            instance.cot_updated_by = cot_updated_by
            instance.save()
            #print('instance',instance)
            module_other = TMasterModuleOther.objects.filter(mmo_other=instance)
            #print('ModuleOther',module_other.query)
            for e_module_other in module_other:
                e_module_other.is_deleted = True
                e_module_other.updated_by = updated_by
                e_module_other.save()
            return instance
        except Exception as e:
            raise e