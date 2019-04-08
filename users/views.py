from django.shortcuts import render
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Permission
from django.contrib.auth.models import *
from users.models import *
from users.serializers import *
from rest_framework.response import Response
from rest_framework import viewsets,status
from rest_framework.views import APIView
from rest_framework import filters

# permission checking
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
# collections 
import collections
#get_current_site
from django.contrib.sites.shortcuts import get_current_site
from mailsend.views import *
from rest_framework.exceptions import APIException

from threading import Thread #for threading
from django.conf import settings
from django.db.models import Q
# pagination
from pagination import CSLimitOffestpagination,CSPageNumberPagination


class LoginAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        try:
            error_msg = "Unable to log in with provided credentials .."
            suspended_msg = "user is suspended .."
            success_msg = "Log in Successfully .."
            # ===========================for contact_no=========================== #
            from django.http import QueryDict
            request_dict = request.data
            request_dict['username'] = request_dict['username'].strip()
            request_dict['password'] = request_dict['password'].strip()
            # ===========================for is_active check=========================== #
            user_status = User.objects.filter(username=request_dict['username']).values("is_active")
            if user_status:
                for u_data in user_status:
                    print("u_data: ", u_data)
                    if not u_data['is_active']:
                        raise APIException(suspended_msg)
            else:
                raise APIException(error_msg)
            # ===========================for is_active check=========================== #
            if request_dict['username'].isnumeric() and len(request_dict['username']) <= 15:
                user_details_data = TCoreUserDetail.objects.filter(cu_phone_no=int(request_dict['username']))\
                    .values("cu_user__username")
                print("fgdfgdf: ",list(user_details_data)[0]['cu_user__username'])
                data = "username={}&password={}".format(str(list(user_details_data)[0]['cu_user__username']),
                                                    request_dict['password'])
                request_dict = QueryDict(data)
            # ===========================for credentials check=========================== #
            try:
                response = super(LoginAuthToken, self).post(request_dict, *args, **kwargs)
            except Exception as error:
                print(error)
                raise APIException(error_msg)
            # ===========================for credentials check=========================== #
            # ===========================for contact_no=========================== #             
            # response = super(LoginAuthToken, self).post(request, *args, **kwargs)
            print("request_qdict: ", request_dict)
            token = Token.objects.get(key=response.data['token'])
            user = User.objects.get(id=token.user_id)
            update_last_login(None, user)
            serializer = UserLoginSerializer(user, many=True)

            # mmr_details = TMasterModuleRole.objects.filter(~Q(mmr_module__cm_permissions_id = settings.PRIVET_PERMISSION_ID)).filter(mmr_user=user)
            mmr_details = TMasterModuleRole.objects.filter(mmr_user=user)
            applications = list()
            for mmr_data in mmr_details:
                module_dict = collections.OrderedDict()
                module_dict["id"] = mmr_data.id
                module_dict["module"] = collections.OrderedDict({
                "id":mmr_data.mmr_module.id,
                "cm_name": mmr_data.mmr_module.cm_name,
                "cm_url": mmr_data.mmr_module.cm_url,
                "cm_icon": "http://"+get_current_site(request).domain + mmr_data.mmr_module.cm_icon.url,
                "permissions":collections.OrderedDict({
                        "id":mmr_data.mmr_module.cm_permissions.id,
                        "cp_u": mmr_data.mmr_module.cm_permissions.cp_u,
                        "cp_g": mmr_data.mmr_module.cm_permissions.cp_g,
                        "cp_o": mmr_data.mmr_module.cm_permissions.cp_o,
                    })
                })
                
                module_dict["role"] = collections.OrderedDict({
                    "id":mmr_data.mmr_role.id,
                    "cr_name":mmr_data.mmr_role.cr_name,
                    "cr_parent_id":mmr_data.mmr_role.cr_parent_id,
                })
                module_dict["permissions"] = collections.OrderedDict({
                    "id":mmr_data.mmr_permissions.id,
                    "cp_u": mmr_data.mmr_permissions.cp_u,
                    "cp_g": mmr_data.mmr_permissions.cp_g,
                    "cp_o": mmr_data.mmr_permissions.cp_o,
                    })
                

                applications.append(module_dict)
            if user:
                user_details = TCoreUserDetail.objects.get(cu_user=user)
                profile_pic = "http://"+get_current_site(request).domain +user_details.cu_profile_img.url if user_details.cu_profile_img else ''
                odict = collections.OrderedDict()
                odict['user_id'] = user.pk
                odict['token'] = token.key
                odict['username'] = user.username
                odict['first_name'] = user.first_name
                odict['last_name'] = user.last_name
                odict['email'] = user.email
                odict['is_superuser'] = user.is_superuser
                odict['cu_super_set'] = user_details.cu_super_set
                odict['cu_phone_no'] = user_details.cu_phone_no
                odict['cu_profile_img'] = profile_pic
                odict['module_access'] = applications
                odict['request_status'] = 1
                odict['msg'] = success_msg

                return Response(odict)
        except Exception as e:
            print("error:", e)
            raise APIException({'request_status': 0, 'msg': e})

class UsersSignInListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    # pagination_class =CSPageNumberPagination
    queryset =User.objects.all()
    serializer_class = UserCreateSerializer

class ChangePasswordView(generics.UpdateAPIView):
    """
    For changing password.
    password is changing using login user token.
    needs old password and new password,
    check old password is exiest or not 
    if exiest than it works
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({'request_status': 1, 'msg': "Wrong password..."}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({'request_status': 0, 'msg': "New Password Save Success..."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Logout(APIView):
    """
        View for user logout
        And delete auth_token
        Using by login user token
        """
    def get(self, request, format=None):        
        request.user.auth_token.delete()
        return Response({'request_status': 0, 'msg': "Logout Success..."}, status=status.HTTP_200_OK)

class ForgotPasswordView(APIView):
    """ 
    Forgot password using mail id ,
    randomly set password,
    mail send using thread,
    using post method
    """

    model = User
    permission_classes = []
    authentication_classes = []
    def post(self, request, format=None):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user_exiest = User.objects.get(email=serializer.data.get("mail_id"))
                print('is_exiest: ', user_exiest)
            except Exception as e:                
                raise APIException({'request_status': 1, 'msg': "User does not exist."})
            password = User.objects.make_random_password()
            # print("password: ", password)                
            user_exiest.set_password(password)
            user_exiest.save()
            # ============= mail Send ==============
            mail_data = {"name": user_exiest.first_name+ '' +user_exiest.last_name, 
            "user": serializer.data.get("mail_id"), 
            "pass": password}
            gmsend = GlobleMailSend('FP001', [serializer.data.get("mail_id")])
            thread = Thread(target = gmsend.mailsend, args = (mail_data,))
            thread.start()
            # ============= sms Send ==============
            # sms_class = GlobleSmsSend("wellcom001", ["8016303114","9038698174"])
            # sms_thread = Thread(target = sms_class.sms_send, args = (mail_data,))
            # sms_thread.start()
            
            return Response({'request_status': 0, 'msg': "New Password Save Success..."}, status=status.HTTP_200_OK)
        return Response({'request_status': 0, 'msg': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ActiveInactiveUserView(generics.RetrieveUpdateAPIView):
    """
    View for user update active and in_active
    using user ID
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class EditUserView(generics.RetrieveUpdateAPIView):
    """
    View for user update 
    using user ID
    login user and provided user must be same..
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = EditUserSerializer
    lookup_field = 'cu_user_id'
    # queryset = TCoreUserDetail.objects.all()
    def get_queryset(self):
        user_id = self.kwargs["cu_user_id"]
        if str(self.request.user.id) == user_id:
            return TCoreUserDetail.objects.filter(cu_user_id = user_id)
        else:
            raise APIException({'request_status': 0, 'msg': 'Login user is different'})


class ModuleUserList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = TCoreUserDetail.objects.filter(cu_user__is_active=True).order_by('cu_user_id')
    serializer_class = UserModuleSerializer
    pagination_class = CSPageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('cu_user__username', 'cu_phone_no', 'cu_alt_phone_no',
                     'cu_emp_code', 'cu_super_set')
    def get_queryset(self):
        try:
            order_by = self.request.query_params.get('order_by', None)
            field_name = self.request.query_params.get('field_name', None)

            if order_by and order_by.lower() == 'desc' and field_name:
                queryset = self.queryset.order_by('-'+field_name)
            elif order_by and order_by.lower() == 'asc' and field_name:
                queryset = self.queryset.order_by(field_name)
            else:
                queryset = self.queryset
            return queryset.filter(~Q(cu_user_id=self.request.user.id))

        except Exception as e:
            # raise e
            raise APIException({'request_status': 0, 'msg': e})