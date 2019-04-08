from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from master.models import *
from core.models import *
from core.serializers import *
from users.serializers import *
from django.contrib.auth.models import *
from rest_framework.exceptions import APIException
from django.conf import settings
import random
import string

class UserListSerializer(serializers.ModelSerializer):
    mmr_role = TCoreRoleSerializer()
    mmr_module = TCoreModuleSerializer()
    mmr_permissions = TCorePermissionsSerializer()
    mmr_user = UserSerializer()
    # mmr_user = UserDetailsSerializer(many=True, read_only=True)


    class Meta:
        model = TMasterModuleRole        
        # fields = ('id','mmr_module', 'mmr_permissions','mmr_role','mmr_user', 'user_details')
        fields = ('id', 'mmr_module', 'mmr_permissions', 'mmr_role', 'mmr_user')


class ModuleRoleSerializer(serializers.ModelSerializer):
    mmr_role = TCoreRoleSerializer()
    class Meta:
        model = TMasterModuleRole        
        fields = ('id','mmr_module', 'mmr_role')
    def create(self, validated_data):
        try:
            data = {}
            logdin_user_id = self.context['request'].user.id
            role_dict = validated_data.pop('mmr_role')

            # print('validated_data: ', validated_data['mmr_module'])
            role = TCoreRole.objects.create(**role_dict, cr_created_by_id=logdin_user_id)
            if role:
                module_role_data = TMasterModuleRole.objects.create(mmr_module = validated_data['mmr_module'], mmr_role=role)
                data['id'] = module_role_data.pk
                data['mmr_module'] = module_role_data.mmr_module
                data['mmr_role'] = module_role_data.mmr_role            

            return data
        except Exception as e:
            # raise e
            raise serializers.ValidationError({'request_status': 0, 'msg': 'error', 'error': e})

# ::::::::::::::::::::::Manpower serializer:::::::::::::::::::::::::::::::::::::::::::

class UserModuleWiseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TMasterModuleRole
        fields = ('id', 'mmr_module','mmr_role', 'mmr_user')

#:::::::::::::::::::::::TMasterModuleGroup::::::::::::::::::::::::::::::::#
class TMasterModuleGroupSerializer(serializers.ModelSerializer):
    mmg_created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    mmg_module_id =serializers.IntegerField(required=True)


    class Meta:
        model = TMasterModuleGroup
        fields = ('id', 'mmg_name', 'mmg_module_id', 'mmg_created_by')

    def create(self, validated_data):
        print('validated_data',validated_data)
        try:
            group_code = 'G-' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
            print('group_code', group_code)
            t_master_module = TMasterModuleGroup.objects.create(**validated_data, mmg_group_code=group_code)
            return t_master_module
        except Exception as e:
            return  e
class TMasterModuleGroupEditSerializer(serializers.ModelSerializer):
    mmg_updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    mmg_name = serializers.CharField(required=False)
    mmg_module = serializers.CharField(required=False)

    class Meta:
        model = TMasterModuleGroup
        fields = ('id', 'mmg_name', 'mmg_module', 'mmg_updated_by')
class TMasterModuleGroupDeleteSerializer(serializers.ModelSerializer):
    mmg_updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    mmr_module = serializers.CharField(required=False)
    mmg_group_code = serializers.CharField(required=False)

    class Meta:
        model = TMasterModuleGroup
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.mmg_is_deleted = True
        instance.mmg_updated_by = validated_data.get('mmg_updated_by')
        instance.save()
        return instance
            

 