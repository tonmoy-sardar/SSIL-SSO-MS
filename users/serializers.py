from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from users.models import *
from django.contrib.auth.models import *
from rest_framework.exceptions import APIException
from core.models import *
from master.models import *
from nameparser import HumanName

from mailsend.views import *
from smssend.views import *

from threading import Thread          #for threading
import os
from django.db import transaction, IntegrityError




class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',
            'password',)

class UserDetailsSerializer(serializers.ModelSerializer):
    # cu_user = UserSerializer()
    class Meta:
        model = TCoreUserDetail
        fields = ('id', 'cu_super_set','cu_emp_code')

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    is_superuser = serializers.BooleanField(required=False)
    is_active = serializers.BooleanField(required=False)
    class Meta:
        model = User
        fields = ('id','first_name', 'last_name', 'username', 'is_superuser', 'is_active')

class UserCreateSerializer(serializers.ModelSerializer):
    """ 
    This Serializer is for Adding User , 
    TCoreUserDetail and TMasterModuleRole table, 
    with the permission id 
    """
    name = serializers.CharField(required=False)
    cu_super_set = serializers.CharField(required=False)
    cu_phone_no = serializers.CharField(required=False)
    cu_emp_code = serializers.CharField(required=False, allow_blank=True)
    role_module_list = serializers.ListField(required=False)
 
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'cu_super_set','cu_phone_no', 'cu_emp_code',
            'role_module_list')
        

    def create(self, validated_data):
        try:
            logdin_user_id = self.context['request'].user.id
            print("logdin_user_id: ", logdin_user_id)
            cu_phone_no = validated_data.pop('cu_phone_no')
            cu_emp_code = validated_data.pop('cu_emp_code') if 'cu_emp_code' in validated_data else ''
            print("cu_emp_code: ", cu_emp_code)
            cu_super_set = validated_data.pop('cu_super_set')
            role_module_list = validated_data.pop('role_module_list')
            name = HumanName(validated_data['name'])
            first_name = name.first + " " + name.middle
            last_name = name.last
            email = validated_data['email']

            with transaction.atomic():
                user_details_count = TCoreUserDetail.objects.filter(cu_phone_no=cu_phone_no).count()
                if user_details_count:
                    raise APIException("phone no alrady exiest")
                user = User.objects.create(first_name=first_name.strip(), last_name=last_name.strip(), username=email, email=email)
                password = User.objects.make_random_password()
                user.set_password(password)
                user.save()

                print('password: ', password)
                
                userdetail = TCoreUserDetail.objects.create(cu_user=user, cu_phone_no=cu_phone_no, cu_super_set=cu_super_set, cu_created_by_id=logdin_user_id)

                if cu_emp_code:
                    userdetail.cu_emp_code = cu_emp_code
                    userdetail.save()


                if role_module_list and userdetail:
                    for role_module in role_module_list:
                        role_id = role_module['role_id']
                        mmr_module_id = role_module['mmr_module_id']
                        mmr_permissions_id = role_module['mmr_permissions_id']

                        mmr_obj=TMasterModuleRole.objects.filter(mmr_module_id=mmr_module_id,
                            mmr_role_id = role_id,
                            mmr_user__isnull=True)
                        # print(mmr_obj)
                        if mmr_obj:
                            for obj in mmr_obj:
                                print("obj: ", obj.id)
                                obj.mmr_user = user
                                obj.mmr_permissions_id = mmr_permissions_id
                                obj.save()

                data = {'id': user.id,
                'name': user.first_name + ' ' + user.last_name,
                'email':user.email,
                'cu_super_set': userdetail.cu_super_set,
                'cu_emp_code': userdetail.cu_emp_code,
                'cu_phone_no': userdetail.cu_phone_no
                }



                # ============= Mail Send ==============
                mail_data = {"name": user.first_name+ '' + user.last_name,
                    "user": email,
                    "pass": password}

                mail_class = GlobleMailSend('FP001', [email])
                mail_thread = Thread(target = mail_class.mailsend, args = (mail_data,))
                mail_thread.start()
                # ============= sms Send ==============
                # sms_class = GlobleSmsSend("wellcom001", [cu_phone_no])
                # sms_thread = Thread(target = sms_class.sms_send, args = (mail_data,))
                # sms_thread.start()

            return data
        except Exception as e:
            # raise e
            raise APIException({'request_status': 0, 'msg': e})

class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ForgotPasswordSerializer(serializers.Serializer):
    """
    Serializer for password forgot.
    """
    mail_id = serializers.CharField(required=True)


class EditUserSerializer(serializers.ModelSerializer):
    cu_updated_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    name = serializers.CharField(required=False)
    cu_user = UserSerializer(read_only=True,required=False)
    class Meta:
        model = TCoreUserDetail
        fields = ('id', 'cu_phone_no', 'cu_alt_phone_no', 'cu_profile_img', 'cu_dob', 'name','cu_updated_by', 'cu_user')
        # lookup_field = 'cu_user_id'


    def update(self, instance, validated_data):
        try:
            name = HumanName(validated_data.pop('name'))
            first_name = name.first + " " + name.middle
            last_name = name.last
            instance.cu_phone_no = validated_data.get("cu_phone_no", instance.cu_phone_no)
            instance.cu_alt_phone_no = validated_data.get("cu_alt_phone_no", instance.cu_alt_phone_no)

            existing_images = './media/' + str(instance.cu_profile_img)
            if validated_data.get('cu_profile_img'):
                print('os.path.isfile(existing_images)::', os.path.isfile(existing_images))
                if os.path.isfile(existing_images):
                    os.remove(existing_images)

                instance.cu_profile_img = validated_data.get("cu_profile_img", instance.cu_profile_img)
            instance.cu_dob = validated_data.get("cu_dob", instance.cu_dob)
            instance.cu_updated_by = validated_data.get("cu_updated_by", instance.cu_updated_by)
            instance.cu_user.first_name = first_name.strip()
            instance.cu_user.last_name = last_name.strip()
            instance.cu_user.save()
            instance.save()

            data_dict = {}
            user_details = TCoreUserDetail.objects.get(pk=instance.id)
            data_dict['id'] = user_details.id
            data_dict['cu_phone_no'] = user_details.cu_phone_no
            data_dict['cu_alt_phone_no'] = user_details.cu_alt_phone_no
            data_dict['cu_profile_img'] = user_details.cu_profile_img
            data_dict['cu_dob'] = user_details.cu_dob
            data_dict['name'] = user_details.cu_user.first_name + " " + user_details.cu_user.last_name
            return data_dict
        except Exception as e:
            raise APIException({'request_status': 0, 'msg': e})

# class AuthUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'email',)
class UserModuleSerializer(serializers.ModelSerializer):
    cu_user = UserSerializer()
    class Meta:
        model = TCoreUserDetail
        fields = ('id', 'cu_emp_code', 'cu_phone_no', 'cu_alt_phone_no', 'cu_dob', 'cu_super_set', 'cu_user', 'applications')




