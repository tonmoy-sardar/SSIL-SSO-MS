from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from pms.models import *
from pms.serializers import *
import time
from multiplelookupfields import MultipleFieldLookupMixin
from rest_framework.views import APIView
from django.conf import settings
from pagination import CSLimitOffestpagination,CSPageNumberPagination
from rest_framework import filters
import calendar
from datetime import datetime
from holidays.models import *
import collections
from rest_framework.exceptions import APIException
import pandas as pd
import numpy as np
from django_filters.rest_framework import DjangoFilterBackend
from master.serializers import UserModuleWiseListSerializer
from master.models import TMasterModuleGroup,TMasterModuleRole
from users.models import TCoreUserDetail
from custom_decorator import response_modify_decorator




#::::::::::::::: TENDER AND TENDER DOCUMENTS :::::::::::::::#
class TendersAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = TendersAddSerializer
class TenderDocsAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = TenderDocumentAddSerializer
class TenderDocsByTenderIdView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = TenderDocumentAddSerializer
    def get_queryset(self):
        tender_id = self.kwargs['tender_id']
        if tender_id:
            queryset = PmsTenderDocuments.objects.filter(tender_id=tender_id).order_by('-created_at')
            return queryset
class TenderEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenders.objects.all()
    serializer_class = TenderEditSerializer
class TenderDocsEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderDocuments.objects.all()
    serializer_class = TenderDocsEditSerializer
class TenderDeleteByIdView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderDocuments.objects.all()
    serializer_class = TenderDeleteSerializer
class TenderDocsDeleteByIdView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderDocuments.objects.all()
    serializer_class = TenderDocumentDeleteSerializer

#::::::::::::::: TENDER  BIDDER TYPE :::::::::::::::#
class VendorsAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = VendorsAddSerializer
    queryset = PmsTenderVendors.objects.all()
class TendorBidderTypeAddView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = TendorBidderTypeAddSerializer
class TendorBidderTypeByTenderIdView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    #serializer_class = TendorBidderTypeByTenderIdSerializer
    def get(self, request, *args, **kwargs):
        print('self',self)
        tender_id = self.kwargs['tender_id']
        if tender_id:
            tender_bidder_data = PmsTenderBidderType.objects.filter(tender=tender_id)
            if tender_bidder_data:
                for each_tender_bidder_data in tender_bidder_data:
                    vendors = []
                    vendors_m_details = PmsTenderBidderTypeVendorMapping.objects.\
                        filter(tender_bidder_type=each_tender_bidder_data.id)
                    #print('vendors_m_details',vendors_m_details)
                    if vendors_m_details:
                        for e_vendors_m_details in vendors_m_details:
                            vendor_d = {
                                "tendor_vendor_id":e_vendors_m_details.tender_vendor.id
                            }
                            vendors.append(e_vendors_m_details.tender_vendor.id)
                    if each_tender_bidder_data.updated_by:
                        updated_by = each_tender_bidder_data.updated_by.id
                    else:
                        updated_by = ''

                    response = {
                        "id":each_tender_bidder_data.id,
                        "bidder_type":each_tender_bidder_data.bidder_type,
                        "type_of_partner": each_tender_bidder_data.type_of_partner,
                        "responsibility": each_tender_bidder_data.responsibility,
                        "profit_sharing_ratio_actual_amount": each_tender_bidder_data.profit_sharing_ratio_actual_amount,
                        "profit_sharing_ratio_tender_specific_amount": each_tender_bidder_data.profit_sharing_ratio_tender_specific_amount,
                        "updated_by":updated_by,
                        "vendors":vendors
                    }
                    return Response(response)
            else:
                return Response()
    def update(self, request, *args, **kwargs):
        tender_id = self.kwargs['tender_id']
        print('request',request.data['bidder_type'])
        try:
            if tender_id:
                tender_bidder_type_vendor_mapping_list = []
                tender_bidder_data = PmsTenderBidderType.objects.get(tender=tender_id)
                print('tender_bidder_data',type(tender_bidder_data))
                with transaction.atomic():
                    if request.data['bidder_type'] == "joint_venture":
                        tender_bidder_data.bidder_type = request.data['bidder_type']
                        tender_bidder_data.type_of_partner=request.data['type_of_partner']
                        tender_bidder_data.responsibility=request.data['responsibility']
                        tender_bidder_data.profit_sharing_ratio_actual_amount=request.data['profit_sharing_ratio_actual_amount']
                        tender_bidder_data.profit_sharing_ratio_tender_specific_amount=request.data['profit_sharing_ratio_tender_specific_amount']
                        tender_bidder_data.updated_by=self.request.user
                        tender_bidder_data.save()
                        xyz=PmsTenderBidderTypeVendorMapping.objects.filter(tender_bidder_type_id=tender_bidder_data.id).delete()
                        print('xyz',xyz)
                        for vendor in request.data['vendors']:
                            print('vendor',vendor)
                            request_dict = {
                                "tender_bidder_type_id": str(tender_bidder_data.id),
                                "tender_vendor_id": int(vendor),
                                "status": True,
                                "created_by": self.request.user,
                                "owned_by": self.request.user
                            }
                            tender_bidder_type_vendor_m = PmsTenderBidderTypeVendorMapping.objects.create(
                                **request_dict)
                        response = {
                            'id': tender_bidder_data.id,
                            'tender': tender_bidder_data.tender.id,
                            'bidder_type': tender_bidder_data.bidder_type,
                            'type_of_partner':  tender_bidder_data.type_of_partner,
                            'responsibility': tender_bidder_data.responsibility,
                            'profit_sharing_ratio_actual_amount':  tender_bidder_data.profit_sharing_ratio_actual_amount,
                            'profit_sharing_ratio_tender_specific_amount':  tender_bidder_data.profit_sharing_ratio_tender_specific_amount,
                            'vendors': request.data['vendors']
                        }
                        return Response(response)
                    else:
                        tender_bidder_data.bidder_type = request.data['bidder_type']
                        tender_bidder_data.responsibility = request.data['responsibility']
                        tender_bidder_data.updated_by = self.request.user
                        tender_bidder_data.save()
                        response = {
                            'id': tender_bidder_data.id,
                            'tender': tender_bidder_data.tender.id,
                            'bidder_type': tender_bidder_data.bidder_type,
                            'responsibility': tender_bidder_data.responsibility,
                        }
                        return Response(response)

        except Exception as e:
            raise e
class TendorBidderTypeEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderBidderType.objects.all()
    serializer_class = TendorBidderTypeEditSerializer
class TendorBidderTypeDeleteView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderBidderType.objects.all()
    serializer_class = TendorBidderTypeDeleteSerializer

#::::::::::::::: TENDER  ELIGIBILITY :::::::::::::::#
class PmsTenderEligibilityFieldsByTypeListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = PmsTenderEligibilityFieldsByTypeEditSerializer
    queryset = PmsTenderEligibilityFieldsByType.objects.all()
    def get_queryset(self):
        tender_id = self.kwargs['tender_id']
        eligibility_type = self.kwargs['eligibility_type']
        return self.queryset.filter(tender_id=tender_id, tender_eligibility__type=eligibility_type,
                                    status=True, is_deleted=False)
class PmsTenderEligibilityAdd(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = PmsTenderEligibilityAddSerializer
    queryset = PmsTenderEligibility.objects.all()
class PmsTenderEligibilityFieldsByTypeEdit(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = PmsTenderEligibilityFieldsByTypeEditSerializer
    queryset = PmsTenderEligibilityFieldsByType.objects.all()
class PmsTenderNotEligibilityReasonAdd(MultipleFieldLookupMixin, generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = PmsTenderNotEligibilityReasonAddSerializer
    queryset = PmsTenderEligibility.objects.filter(status=True, is_deleted=False)
    lookup_fields = ("tender_id", "type")

#::::::::::::::: TENDER SURVEY SITE PHOTOS:::::::::::::::#
class TenderSurveySitePhotosAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveySitePhotos.objects.all()
    serializer_class =TenderSurveySitePhotosAddSerializer
class TenderSurveySitePhotosEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveySitePhotos.objects.all()
    serializer_class =TenderSurveySitePhotosEditSerializer
class TenderSurveySitePhotosListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveySitePhotos.objects.all()
    serializer_class =TenderSurveySitePhotosListSerializer
    def get_queryset(self):
        tender_id = self.kwargs['tender_id']
        queryset = PmsTenderSurveySitePhotos.objects.filter(tender_id=tender_id, status=True)
        return queryset
class TenderSurveySitePhotosDeleteView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveySitePhotos.objects.all()
    serializer_class =TenderSurveySitePhotosDeleteSerializer

#::::::::::::::: TENDER SURVEY COORDINATE :::::::::::::::#
class TenderSurveyLocationAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyCoordinatesSiteCoordinate.objects.all()
    serializer_class =TenderSurveyLocationAddSerializer
class TenderSurveyLocationListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyCoordinatesSiteCoordinate.objects.all()
    serializer_class =TenderSurveyLocationListSerializer
    def get_queryset(self):
        tender_id=self.kwargs['tender_id']
        queryset = PmsTenderSurveyCoordinatesSiteCoordinate.objects.filter(
            tender_id=tender_id,status=True,is_deleted=False)
        return queryset
class TenderSurveyLocationEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyCoordinatesSiteCoordinate.objects.all()
    serializer_class =TenderSurveyLocationEditSerializer
class TenderSurveyLocationDeleteView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyCoordinatesSiteCoordinate.objects.all()
    serializer_class =TenderSurveyLocationDeleteSerializer
class TenderSurveyCOSupplierListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    #pagination_class = CSPageNumberPagination
    queryset = PmsTenderSurveyCoordinatesSuppliers.objects.all()
    serializer_class =TenderSurveyCOSupplierListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('type','tender_survey_material','tender')
    @response_modify_decorator
    def list(self, request, *args, **kwargs):
        return response
class TenderSurveyCOSupplierAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyCoordinatesSuppliers.objects.all()
    serializer_class =TenderSurveyCOSupplierAddSerializer
class TenderSurveyCOSupplierEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyCoordinatesSuppliers.objects.all()
    serializer_class =TenderSurveyCOSupplierEditSerializer
class TenderSurveyCOSupplierDeleteView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyCoordinatesSuppliers.objects.all()
    serializer_class =TenderSurveyCOSupplierDeleteSerializer
class TenderSurveyCOSupplierDocumentAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyCoordinatesSuppliersDocument.objects.all()
    serializer_class = TenderSurveyCOSupplierDocumentAddSerializer
class TenderSurveyCOSupplierDocumentEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyCoordinatesSuppliersDocument.objects.all()
    serializer_class = TenderSurveyCOSupplierDocumentEditSerializer
class TenderSurveyCOSupplierDocumentDeleteView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyCoordinatesSuppliersDocument.objects.all()
    serializer_class = TenderSurveyCOSupplierDocumentDeleteSerializer

#::::::::::: TENDER SURVEY METERIAL ::::::::::::::::::::#
class TenderSurveyMaterialsAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyMaterials.objects.all()
    serializer_class=TenderSurveyMaterialsAddSerializer
class TenderSurveyMaterialsEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyMaterials.objects.all()
    serializer_class=TenderSurveyMaterialsEditSerializer
class TenderSurveyMaterialsDeleteView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyMaterials.objects.all()
    serializer_class = TenderSurveyMaterialsDeleteSerializer
class TenderSurveyMaterialsListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyMaterials.objects.filter(status=True)
    serializer_class = TenderSurveyMaterialsListSerializer
class TenderSurveyMaterialsListByTenderView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyMaterials.objects.filter(status=True)
    serializer_class = TenderSurveyMaterialsListSerializer
    def get_queryset(self):
        tender_id=self.kwargs['tender_id']
        print('tender_id',tender_id)
        return self.queryset.filter(tender_id=tender_id,status=True,is_deleted=False)

#::::::::::: TENDER SURVEY RESOURCE METERIAL SUPPLIERS ::::::::::::::::::::#
class TenderSurveyResourceMaterialAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyResourceMaterial.objects.all()
    serializer_class= TenderSurveyResourceMaterialAddSerializer
class TenderSurveyResourceMaterialEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyResourceMaterial.objects.all()
    serializer_class= TenderSurveyResourceMaterialEditSerializer
class TenderSurveyResourceMaterialDeleteView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyResourceMaterial.objects.all()
    serializer_class= TenderSurveyResourceMaterialDeleteSerializer
class TenderSurveyResourceMaterialListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyResourceMaterial.objects.filter(status=True)
    serializer_class = TenderSurveyResourceMaterialListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('tender', 'tender_survey_material')
    def list(self, request, *args, **kwargs):
        response = super(TenderSurveyResourceMaterialListView, self).list(request, args, kwargs)
        data_dict = {}
        data_dict['result'] = response.data
        if response.data:
            data_dict['request_status'] = 1
            data_dict['msg'] = settings.MSG_SUCCESS
        elif len(response.data) == 0:
            data_dict['request_status'] = 1
            data_dict['msg'] = settings.MSG_NO_DATA
        else:
            data_dict['request_status'] = 0
            data_dict['msg'] = settings.MSG_ERROR

        response.data = data_dict
        return response
class TenderSurveyResourceMaterialDocumentAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyResourceMaterialDocument.objects.all()
    serializer_class = TenderSurveyResourceMaterialDocumentAddSerializer
class TenderSurveyResourceMaterialDocumentEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyResourceMaterialDocument.objects.all()
    serializer_class = TenderSurveyResourceMaterialDocumentEditSerializer
class TenderSurveyResourceMaterialDocumentDeleteView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyResourceMaterialDocument.objects.all()
    serializer_class = TenderSurveyResourceMaterialDocumentDeleteSerializer


#:::::::::: TENDER SURVEY RESOURCE ESTABLISHMENT :::::::::::#
class TenderSurveyResourceEstablishmentAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyResourceEstablishment.objects.filter(status=True,is_deleted=False)
    serializer_class = TenderSurveyResourceEstablishmentAddSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('tender',)
    @response_modify_decorator
    def list(self, *args, **kwargs):
        return response
    def get(self, request, *args,**kwargs):
        response = super(TenderSurveyResourceEstablishmentAddView, self).get(self, request, args, kwargs)
        data_dict={}
        data_dict['result'] = response.data
        establishment_document=PmsTenderSurveyDocument.objects.filter(
            model_class="PmsTenderSurveyResourceEstablishment",
            status=True,is_deleted=False)
        document_details=list()
        for document in establishment_document:
            data={
                "id":int(document.id),
                "tender":int(document.tender.id),
                "module_id":document.module_id,
                "document_name":document.document_name,
                "document":request.build_absolute_uri(document.document.url),
            }
            document_details.append(data)

        data_dict['result']['establishment_document_details']=document_details

        response.data = data_dict
        return response




class TenderSurveyResourceEstablishmentEditView(generics.RetrieveUpdateAPIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [TokenAuthentication]
	queryset = PmsTenderSurveyResourceEstablishment.objects.all()
	serializer_class = TenderSurveyResourceEstablishmentEditSerializer
class TenderSurveyResourceEstablishmentDeleteView(generics.RetrieveUpdateAPIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [TokenAuthentication]
	queryset = PmsTenderSurveyResourceEstablishment.objects.all()
	serializer_class = TenderSurveyResourceEstablishmentDeleteSerializer
class TenderSurveyResourceEstablishmentDocumentAddView(generics.ListCreateAPIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [TokenAuthentication]
	queryset = PmsTenderSurveyDocument.objects.filter(status=True,is_deleted=False)
	serializer_class =TenderSurveyResourceEstablishmentDocumentAddSerializer
class TenderSurveyResourceEstablishmentDocumentEditView(generics.RetrieveUpdateAPIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [TokenAuthentication]
	queryset = PmsTenderSurveyDocument.objects.all()
	serializer_class =TenderSurveyResourceEstablishmentDocumentEditSerializer
class TenderSurveyResourceEstablishmentDocumentDeleteView(generics.RetrieveUpdateAPIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [TokenAuthentication]
	queryset = PmsTenderSurveyDocument.objects.all()
	serializer_class =TenderSurveyResourceEstablishmentDocumentDeleteSerializer

#:::: TENDER SURVEY RESOURCE HYDROLOGICAL :::::::#
class TenderSurveyResourceHydrologicalAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = TenderSurveyResourceHydrologicalAddSerializer
    queryset = PmsTenderSurveyResourceHydrological.objects.filter(status=True, is_deleted=False)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('tender',)
    @response_modify_decorator
    def list(self, request, *args, **kwargs):
        return response
class TenderSurveyResourceHydrologicalEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = TenderSurveyResourceHydrologicalEditSerializer
    queryset = PmsTenderSurveyResourceHydrological.objects.filter(status=True, is_deleted=False)
class TenderSurveyResourceHydrologicalDeleteView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = TenderSurveyResourceHydrologicalDeleteSerializer
    queryset = PmsTenderSurveyResourceHydrological.objects.all()
class TenderSurveyResourceHydrologicalDocumentAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = TenderSurveyResourceHydrologicalDocumentAddSerializer
    queryset = PmsTenderSurveyDocument.objects.all()
class TenderSurveyResourceHydrologicalDocumentEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = TenderSurveyResourceHydrologicalDocumentEditSerializer
    queryset = PmsTenderSurveyDocument.objects.filter(status=True, is_deleted=False)
class TenderSurveyResourceHydrologicalDocumentDeleteView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = TenderSurveyResourceHydrologicalDocumentDeleteSerializer
    queryset = PmsTenderSurveyDocument.objects.all()

#:::: TENDER SURVEY RESOURCE CONTRACTORS / VENDORS :::::::#
class TenderSurveyResourceContractorsOVendorsContractorAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyResourceContractorsOVendorsContractor.objects.all()
    serializer_class =TenderSurveyResourceContractorsOVendorsContractorAddSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('tender',)
    @response_modify_decorator
    def list(self, request, *args, **kwargs):
        return response
class TenderSurveyResourceContractorsOVendorsContractorEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyResourceContractorsOVendorsContractor.objects.all()
    serializer_class = TenderSurveyResourceContractorsOVendorsContractorEditSerializer
class TenderSurveyResourceContractorsOVendorsContractorDeleteView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyResourceContractorsOVendorsContractor.objects.all()
    serializer_class = TenderSurveyResourceContractorsOVendorsContractorDeleteSerializer
class TenderSurveyResourceContractorsOVendorsContractorDocumentAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class =TenderSurveyResourceContractorsOVendorsContractorDocumentAddSerializer
    queryset = PmsTenderSurveyDocument.objects.filter(status=True, is_deleted=False)
class TenderSurveyResourceContractorsOVendorsContractorDocumentEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class =TenderSurveyResourceContractorsOVendorsContractorDocumentEditSerializer
    queryset = PmsTenderSurveyDocument.objects.filter(status=True, is_deleted=False)
class TenderSurveyResourceContractorsOVendorsContractorDocumentDeleteView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class =TenderSurveyResourceContractorsOVendorsContractorDocumentDeleteSerializer
    queryset = PmsTenderSurveyDocument.objects.filter(status=True, is_deleted=False)
class TenderSurveyResourceContractorsOVendorsVendorModelMasterAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class =TenderSurveyResourceContractorsOVendorsVendorModelMasterAddSerializer
    queryset = PmsTenderSurveyResourceContractorsOVendorsVendorModelMaster.objects.filter(status=True, is_deleted=False)
    @response_modify_decorator
    def list(self,*args,**kwargs):
        return response
class TenderSurveyResourceContractorsOVendorsVendorAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = TenderSurveyResourceContractorsOVendorsVendorAddSerializer
    queryset = PmsTenderSurveyResourceContractorsOVendorsVendor.objects.filter(status=True, is_deleted=False)
    @response_modify_decorator
    def list(self,request, *args, **kwargs):
        return response
class TenderSurveyResourceContractorsOVendorsVendorEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = TenderSurveyResourceContractorsOVendorsVendorEditSerializer
    queryset = PmsTenderSurveyResourceContractorsOVendorsVendor.objects.filter(status=True, is_deleted=False)
class TenderSurveyResourceContractorsOVendorsVendorDeleteView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = TenderSurveyResourceContractorsOVendorsVendorDeleteSerializer
    queryset = PmsTenderSurveyResourceContractorsOVendorsVendor.objects.all()
class TenderSurveyResourceContractorsOVendorsVendorDocumentAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = TenderSurveyResourceContractorsOVendorsVendorDocumentAddSerializer
    queryset = PmsTenderSurveyDocument.objects.filter(status=True, is_deleted=False)
class TenderSurveyResourceContractorsOVendorsVendorDocumentEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = TenderSurveyResourceContractorsOVendorsVendorDocumentEditSerializer
    queryset = PmsTenderSurveyDocument.objects.filter(status=True, is_deleted=False)
class TenderSurveyResourceContractorsOVendorsVendorDocumentDeleteView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = TenderSurveyResourceContractorsOVendorsVendorDocumentDeleteSerializer
    queryset = PmsTenderSurveyDocument.objects.filter(status=True, is_deleted=False)

#:::: TENDER SURVEY RESOURCE CONTACT DETAILS AND DESIGNATION :::::::#
class TenderSurveyResourceContactDesignationAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyResourceContactDesignation.objects.filter(status=True)
    serializer_class = TenderSurveyResourceContactDesignationAddSerializer
class TenderSurveyResourceContactDetailsAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyResourceContactDetails.objects.all()
    serializer_class =TenderSurveyResourceContactDetailsAddSerializer
class TenderSurveyResourceContactDetailsEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyResourceContactDetails.objects.all()
    serializer_class =TenderSurveyResourceContactDetailsEditSerializer
class TenderSurveyResourceContactDetailsDeleteView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyResourceContactDetails.objects.all()
    serializer_class =TenderSurveyResourceContactDetailsDeleteSerializer

#::::::::::: TENDER INITIAL COSTING ::::::::::::::::::::#
class TenderInitialCostingUploadFileView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def post(self, request, format=None):
        try:
            field_label_value = []
            #tender_initial_costing=PmsTenderInitialCosting.objects.create(**validated_data)
            import numpy as np
            import pandas as pd
            import xlrd
            df1 = pd.read_excel(request.data['document']) #read excel
            df2 = df1.replace(np.nan,'',regex=True) # for replace blank value with nan
            df =df2.loc[:, ~df2.columns.str.contains('^Unnamed')] # for elmeminate the blank index
            #print("Column headings:")
            #print(df.columns)
            for j in df.columns:
                #print(df[j])
                field_value = []
                # tender_initial_costing_label = PmsTenderInitialCostingExcelFieldLabel.\
                #     objects.create(
                #     tender_initial_costing=PmsTenderInitialCosting.objects.get(pk=1),
                #     field_label=j
                #
                # )
                for i in df.index:
                    # tender_initial_costing_field = PmsTenderInitialCostingExcelFieldValue. \
                    #     objects.create(
                    #     tender_initial_costing=PmsTenderInitialCosting.objects.get(pk=1),
                    #     initial_costing_field_label=tender_initial_costing_label,
                    #     field_value=df[j][i]
                    #
                    # )
                    field_value.append(df[j][i])
                field_label_val_dict = {
                        "field_label":j,
                        "field_value":field_value

                }
                    #print(df[j][i])
                field_label_value.append(field_label_val_dict)
            #print('field_label_value',field_label_value)
            response_data={
                "tender":request.data['tender'],
                "field_label_value":field_label_value
            }
            return Response(response_data)
        except Exception as e:
            raise APIException({'request_status': 0, 'msg': e})
class TenderInitialCostingAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderInitialCosting.objects.all()
    serializer_class =TenderInitialCostingAddSerializer

#:::::::::::: ATTENDENCE ::::::::::::::::::::::::::::#
class AttendanceLoginView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsAttendance.objects.all()
    serializer_class = PmsAttendanceAddSerializer

    def post(self, request, *args, **kwargs):
        response = super(AttendanceLoginView, self).post(request,args,kwargs)
        try:
            response.data['msg'] = settings.MSG_SUCCESS
            response.data['request_status'] = 1
        except Exception as e:
            response.data['msg'] = settings.MSG_ERROR
            response.data['request_status'] = 0

        return response
class AttendanceAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsAttendance.objects.all()
    serializer_class = AttendanceAddSerializer

    def post(self, request, *args,**kwargs):
        response = super(AttendanceAddView, self).post(request, args, kwargs)
        data_dict = {}
        data_dict['result'] = response.data
        if response.data:
            data_dict['request_status'] = 1
            data_dict['msg'] = settings.MSG_SUCCESS
        elif len(response.data) == 0:
            data_dict['request_status'] = 1
            data_dict['msg'] = settings.MSG_NO_DATA
        else:
            data_dict['request_status'] = 0
            data_dict['msg'] = settings.MSG_ERROR

        response.data = data_dict
        return response
class AttendanceListByEmployeeView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    # pagination_class = CSPageNumberPagination
    queryset = PmsAttendance.objects.all()
    serializer_class = AttendanceListSerializer
    filter_backends = (filters.OrderingFilter, filters.SearchFilter,)
    search_fields = ('date', 'employee', 'employee__username', 'login_time', 'logout_time', 'type')
    ordering = ('-created_at',)

    def get_queryset(self):
        employee_id = self.kwargs["employee_id"]
        year = int(self.request.query_params['year']) if 'year' in self.request.query_params else int(
            datetime.today().date().strftime("%Y"))
        month = int(self.request.query_params['month']) if 'month' in self.request.query_params else int(
            datetime.today().date().strftime("%m"))
        return self.queryset.filter(employee_id= employee_id, created_at__year = year, created_at__month=month)

    def get_holidays_list(self):
        holidays_list = HolidaysList.objects.filter(status=True)
        holidays_dict = {}
        for data in holidays_list:
            dt_str = data.holiday_date.strftime('%Y-%m-%d')
            holidays_dict[dt_str] = data.holiday_name
        return holidays_dict

    def list(self, request, *args, **kwargs):
        try:
            holidays_dict = self.get_holidays_list()
            # print("holidays_dict: ", holidays_dict)
            current_date = datetime.today().date()
            year = int(self.request.query_params['year']) if 'year' in self.request.query_params else int(current_date.strftime("%Y"))
            month = int(self.request.query_params['month']) if 'month' in self.request.query_params else int(current_date.strftime("%m"))

            response = super(AttendanceListByEmployeeView, self).list(request, args, kwargs)
            results_data_listofdict = response.data
            month_date_list = self.get_month_dates(year, month)
            absent_date_list = []
            present_date_list = [oddata['date'] for oddata in results_data_listofdict]

            for date in month_date_list:
                if date not in present_date_list:
                    # print(date)
                    present_date = datetime.strptime(date, '%Y-%m-%d').date()
                    rest_day = current_date - present_date
                    if rest_day.days >= 0:
                        absent_date_list.append(date)

            for od in results_data_listofdict:
                # print(od['date'])
                week_day = datetime.strptime(od['date'], '%Y-%m-%dT%H:%M:%S').strftime('%A')
                od['date'] = datetime.strptime(od['date'], '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d')
                od['week_day'] = week_day
                od['present'] = 1
                od['holiday'] = 0

            for absent_date in absent_date_list:
                ab_week_day = datetime.strptime(absent_date, '%Y-%m-%d').strftime('%A')
                data_dict = {
                    "type": 1,
                    "employee": self.kwargs["employee_id"],
                    "user_project": "",
                    "date": absent_date,
                    "login_time": "",
                    "logout_time": "",
                    "approved_status": 0,
                    "justification": "Auto genareted absent",
                    "week_day": ab_week_day,
                    "present": 0,
                    "holiday": 0
                }
                if absent_date in holidays_dict.keys():
                    data_dict["holiday"] = 1
                    data_dict["justification"] = holidays_dict[absent_date]



                results_data_listofdict.append(data_dict)

            response_data_dict = collections.OrderedDict()
            response_data_dict['count'] = len(results_data_listofdict)
            response_data_dict['results'] = results_data_listofdict
            response_data_dict['request_status'] = 1
            response_data_dict['msg'] = settings.MSG_SUCCESS
            # print(response_data_dict)
            return Response(self.list_synchronization(response_data_dict))
        except Exception as e:
            raise APIException({'request_status': 0, 'msg': e})

    def list_synchronization(self, list_data: list)-> list:
        data = pd.DataFrame(list_data["results"])
        data = data.replace(np.nan, 0, regex=True)
        data.sort_values("date", axis = 0, ascending = True, inplace = True,)
        col_list = data.columns.values
        row_list = data.values.tolist()
        total_result = list()
        for row in row_list:
            data_dict = dict(zip(col_list,row))
            total_result.append(data_dict)
        list_data["results"] = total_result
        return list_data


    def get_month_dates(self, year, month)-> list:
        date_list = []
        cal = calendar.Calendar()
        for cal_date in cal.itermonthdates(year, month):
            if cal_date.month == month:
                cal_d = cal_date.strftime('%Y-%m-%d')

                date_list.append(cal_d)
        return date_list
class AttendanceApprovalList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = CSPageNumberPagination
    queryset = PmsAttendance.objects.filter(approved_status=1)
    serializer_class = AttendanceApprovalListSerializer

    def list(self, request, *args, **kwargs):
        response = super(AttendanceApprovalList, self).list(request, args, kwargs)
        response.data['request_status'] = 0
        response.data['msg'] = settings.MSG_ERROR
        response.data['per_page_count'] = len(response.data['results'])
        if response.data['results']:
            response.data['request_status'] = 1
            response.data['msg'] = settings.MSG_SUCCESS
        return response
class AttendanceEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsAttendance.objects.filter(is_deleted=False)
    serializer_class = AttendanceSerializer

    def put(self, request,* args, **kwargs):
        response = super(AttendanceEditView, self).put(request, args, kwargs)
        print('request: ', request.data)
        data_dict = {}
        data_dict['result'] = request.data
        if response.data:
            data_dict['request_status'] = 1
            data_dict['msg'] = settings.MSG_SUCCESS
        # elif len(response.data) == 0:
        #     data_dict['request_status'] = 1
        #     data_dict['msg'] = settings.MSG_NO_DATA
        else:
            data_dict['request_status'] = 0
            data_dict['msg'] = settings.MSG_ERROR

        response.data = data_dict
        return response
class AttendanceLogOutView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsAttendance.objects.filter(is_deleted=False)
    serializer_class = AttendanceLogOutSerializer

    def put(self, request,* args, **kwargs):
        response = super(AttendanceLogOutView, self).put(request, args, kwargs)
        # print('request: ', request.data)
        data_dict = {}
        data_dict['result'] = response.data
        if response.data:
            data_dict['request_status'] = 1
            data_dict['msg'] = settings.MSG_SUCCESS
        else:
            data_dict['request_status'] = 0
            data_dict['msg'] = settings.MSG_ERROR

        response.data = data_dict
        return response
class AttandanceAllDetailsListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsAttendance.objects.all()
    serializer_class = AttandanceALLDetailsListSerializer
    pagination_class = CSPageNumberPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('date', 'employee__username',)
    ordering = ('-id',)
    def get_queryset(self):
        year = int(self.request.query_params['year']) if 'year' in self.request.query_params else int(
            datetime.today().date().strftime("%Y"))
        month = int(self.request.query_params['month']) if 'month' in self.request.query_params else int(
            datetime.today().date().strftime("%m"))
        return self.queryset.filter(created_at__year = year, created_at__month=month)
    def list_synchronization(self, list_data: list)-> list:
        data = pd.DataFrame(list_data)
        data = data.replace(np.nan, 0, regex=True)
        data.sort_values("date", axis = 0, ascending = True, inplace = True,)
        col_list = data.columns.values
        row_list = data.values.tolist()
        total_result = list()
        for row in row_list:
            data_dict = dict(zip(col_list,row))
            total_result.append(data_dict)
        list_data = total_result
        return list_data

    def list(self, request, *args, **kwargs):
        response = super(AttandanceAllDetailsListView, self).list(request,args,kwargs)
        response.data['request_status'] = 0
        response.data['msg'] = settings.MSG_ERROR

        if response.data['results']:
            for data in response.data['results']:
                if not data['user_project']:
                    data['user_project'] = {}
            response.data['results'] = self.list_synchronization(list(response.data['results']))
            response.data['request_status'] = 1
            response.data['msg'] = settings.MSG_SUCCESS
        return response

#:::::::::::: PmsAttandanceLog ::::::::::::::::::::::::::::#
class AttandanceLogAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsAttandanceLog.objects.all()
    serializer_class = AttandanceLogAddSerializer
    pagination_class=CSPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('attandance',)

    def list(self, request, *args, **kwargs):
        response = super(AttandanceLogAddView, self).list(request,args,kwargs)

        if response.data['results']:
            response.data['request_status'] = 1
            response.data['msg'] = settings.MSG_SUCCESS
        elif len(response.data['results']) ==0:
            response.data['request_status'] = 1
            response.data['msg'] = settings.MSG_NO_DATA
        else:
            response.data['request_status'] = 0
            response.data['msg'] = settings.MSG_ERROR

        return response
class AttendanceLogEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsAttandanceLog.objects.all()
    serializer_class = AttandanceLogEditSerializer
class AttandanceLogApprovalEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsAttandanceLog.objects.all()
    serializer_class = AttandanceLogApprovalEditSerializer

#:::::::::::: Pms Attandance leave ::::::::::::::::::::::::::::#
class AdvanceLeaveAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = CSPageNumberPagination
    queryset = PmsEmployeeLeaves.objects.all()
    serializer_class=AdvanceLeavesAddSerializer

    # def post(self, request, *args, **kwargs):
    #     response = super(AdvanceLeaveAddView, self).list(request, args, kwargs)
    #     response.data['request_status'] = 0
    #     response.data['msg'] = settings.MSG_ERROR
    #     response.data['per_page_count'] = len(response.data['results'])
    #     if response.data['results']:
    #         response.data['request_status'] = 1
    #         response.data['msg'] = settings.MSG_SUCCESS
    #     return response

    # def list(self, request, *args, **kwargs):
    #     response = super(AdvanceLeaveAddView, self).list(request, args, kwargs)
    #     response.data['request_status'] = 0
    #     response.data['msg'] = settings.MSG_ERROR
    #     response.data['per_page_count'] = len(response.data['results'])
    #     if response.data['results']:
    #         response.data['request_status'] = 1
    #         response.data['msg'] = settings.MSG_SUCCESS
    #     return response
    # def get(self, request, *args, **kwargs):
    #     response = super(AdvanceLeaveAddView, self).list(request, args, kwargs)
    #     response.data['request_status'] = 0
    #     response.data['msg'] = settings.MSG_ERROR
    #     response.data['per_page_count'] = len(response.data['results'])
    #     if response.data['results']:
    #         response.data['request_status'] = 1
    #         response.data['msg'] = settings.MSG_SUCCESS
    #     return response
class AdvanceLeaveEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsEmployeeLeaves.objects.all()
    serializer_class=AdvanceLeaveEditSerializer
class LeaveListByEmployeeView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = CSPageNumberPagination
    queryset = PmsEmployeeLeaves.objects.all()
    serializer_class = LeaveListByEmployeeSerializer

    def get_queryset(self,*args,**kwargs):
        employee_id=self.kwargs['employee_id']
        print('employee_id',employee_id)
        return self.queryset.filter(employee=employee_id)

    def list(self, request, *args, **kwargs):
        response = super(LeaveListByEmployeeView, self).list(request, args, kwargs)
        response.data['request_status'] = 0
        response.data['msg'] = settings.MSG_ERROR
        response.data['per_page_count'] = len(response.data['results'])
        if response.data['results']:
            response.data['request_status'] = 1
            response.data['msg'] = settings.MSG_SUCCESS
        return response

#:::::::::::::::::::Pms Attandance Deviation::::::::::::::::::::#
class AttandanceDeviationJustificationEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsAttandanceDeviation.objects.all()
    serializer_class = AttandanceDeviationJustificationEditSerializer
class AttandanceDeviationApprovaEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsAttandanceDeviation.objects.all()
    serializer_class = AttandanceDeviationApprovaEditSerializer

#:::::::::::::::::  MECHINARY MASTER :::::::::::::::#
class MachineriesAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsMachineries.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = MachineriesAddSerializer
    def get(self, request, *args, **kwargs):
        response = super(MachineriesAddView, self).get(self, request, args, kwargs)
        for data in response.data:
            if data["owner_type"] == 1:
                machinary_rented_details_queryset = PmsMachinaryRentedDetails.objects.filter(equipment=data["id"],
                                                                                             is_deleted=False)
                rental_details = dict()
                for machinary_rent in machinary_rented_details_queryset:
                    rental_details['id'] = machinary_rent.id
                    rental_details['equipment'] = machinary_rent.equipment.id
                    rental_details['vendor'] = machinary_rent.vendor.id
                    rental_details['rent_amount'] = machinary_rent.rent_amount
                    rental_details['type_of_rent'] = machinary_rent.type_of_rent.id
                if rental_details:
                    data["rental_details"] = rental_details
            elif data["owner_type"] == 2:
                owner_queryset = PmsMachinaryOwnerDetails.objects.filter(equipment=data["id"], is_deleted=False)
                owner_dict = {}
                for owner in owner_queryset:
                    owner_dict['id'] = owner.id
                    owner_dict['equipment'] = owner.equipment.id
                    owner_dict['purchase_date'] = owner.purchase_date
                    owner_dict['price'] = owner.price

                    if owner.is_emi_available:
                        emi_queryset = PmsMachinaryOwnerEmiDetails.objects.filter(equipment_owner_details=owner,
                                                                                  equipment=data["id"],
                                                                                  is_deleted=False)
                        emi_dict = {}
                        for emi in emi_queryset:
                            emi_dict['id'] = emi.id
                            emi_dict['equipment'] = emi.equipment
                            emi_dict['equipment_owner_details'] = emi.equipment_owner_details
                            emi_dict['amount'] = emi.amount
                            emi_dict['start_date'] = emi.start_date
                            emi_dict['no_of_total_installment'] = emi.no_of_total_installment

                        if emi_dict:
                            owner_dict['owner_emi_details'] = emi_dict
                if owner_dict:
                    data['owner_details'] = owner_dict
            elif data["owner_type"] == 3:
                contract_queryset = PmsMachinaryContractDetails.objects.filter(equipment=data["id"], is_deleted=False)
                contract_dict = {}
                for contract in contract_queryset:
                    contract_dict['id'] = contract.id
                    contract_dict['equipment'] = contract.equipment.id
                    contract_dict['contractor'] = contract.contractor.id
                data['contract_details'] = contract_dict
            else:
                pass
        return response
class MachineriesEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsMachineries.objects.all()
    serializer_class = MachineriesEditSerializer
    def get(self, request, *args, **kwargs):
        response = super(MachineriesEditView, self).get(self, request, args, kwargs)
        #print('response', response.data)
        #print('equipment_category', type(response.data['equipment_category']))
        PmsMachineriesWorkingCategoryde = PmsMachineriesWorkingCategory.objects.filter(id=response.data['equipment_category'],
                                                                                       is_deleted=False)
        #print('PmsMachineriesWorkingCategory',PmsMachineriesWorkingCategoryde)
        for e_PmsMachineriesWorkingCategoryde in PmsMachineriesWorkingCategoryde:
            w_c_details = { 'id':e_PmsMachineriesWorkingCategoryde.id,
                            'name':e_PmsMachineriesWorkingCategoryde.name,
                            'is_deleted': e_PmsMachineriesWorkingCategoryde.is_deleted,
                            }

        response.data['equipment_category_details'] = w_c_details
        PmsMachineriesDoc = PmsMachineriesDetailsDocument.objects.filter(
            equipment=response.data['id'],is_deleted=False)
        #print('PmsMachineriesDoc', PmsMachineriesDoc)
        m_d_details_list=[]
        #request = self.context.get('request')
        for e_PmsMachineriesDoc in PmsMachineriesDoc:
            m_d_details = { 'id':e_PmsMachineriesDoc.id,
                            'name':e_PmsMachineriesDoc.document_name,
                            'document': request.build_absolute_uri(e_PmsMachineriesDoc.document.url),
                            'is_deleted': e_PmsMachineriesDoc.is_deleted,
                            }
            m_d_details_list.append(m_d_details)
        #print('m_d_details_list',m_d_details_list)
        response.data['document_details'] = m_d_details_list
        if response.data["owner_type"] == 1:
            # print('xyz',gfsdsdf)
            machinary_rented_details_queryset = PmsMachinaryRentedDetails.objects.filter(equipment=response.data["id"],
                                                                                         is_deleted=False)
            print('machinary_rented_details_queryset',machinary_rented_details_queryset)
            rental_details = dict()
            for machinary_rent in machinary_rented_details_queryset:
                rental_details['id'] = machinary_rent.id
                rental_details['equipment'] = machinary_rent.equipment.id
                rental_details['vendor'] = machinary_rent.vendor.id
                rental_details['rent_amount'] = machinary_rent.rent_amount
                rental_details['type_of_rent'] = machinary_rent.type_of_rent.id
            if rental_details:
                response.data["rental_details"] = rental_details
                m_rented_details_vendor = PmsExternalUsers.objects.filter(
                    pk=machinary_rent.vendor.id,is_deleted=False)
                print('m_rented_details_vendor',m_rented_details_vendor)
                for e_m_rented_details_vendor in m_rented_details_vendor:
                    m_v_details = {'id': e_m_rented_details_vendor.id,
                                   'name': e_m_rented_details_vendor.name,
                                   'is_deleted': e_m_rented_details_vendor.is_deleted,
                                   }
                response.data["rental_details"]['vendor_details']= m_v_details
        elif response.data["owner_type"] == 2:
            owner_queryset = PmsMachinaryOwnerDetails.objects.filter(equipment=response.data["id"], is_deleted=False)
            print('owner_queryset',owner_queryset)
            owner_dict = {}
            for owner in owner_queryset:
                owner_dict['id'] = owner.id
                owner_dict['equipment'] = owner.equipment.id
                owner_dict['purchase_date'] = owner.purchase_date
                owner_dict['price'] = owner.price
                owner_dict['is_emi_available'] = owner.is_emi_available

                if owner.is_emi_available:
                    emi_queryset = PmsMachinaryOwnerEmiDetails.objects.filter(equipment_owner_details=owner,
                                                                              equipment=response.data["id"],
                                                                              is_deleted=False)
                    #print('emi_queryset',emi_queryset)
                    emi_dict = {}
                    for emi in emi_queryset:
                        emi_dict['id'] = emi.id
                        emi_dict['equipment'] = emi.equipment.id
                        emi_dict['equipment_owner_details'] = emi.equipment_owner_details.id
                        emi_dict['amount'] = emi.amount
                        emi_dict['start_date'] = emi.start_date
                        emi_dict['no_of_total_installment'] = emi.no_of_total_installment

                    if emi_dict:
                        owner_dict['owner_emi_details'] = emi_dict
                        print('owner_dict',owner_dict)
            if owner_dict:
                response.data['owner_details'] = owner_dict
        else:
            contract_queryset = PmsMachinaryContractDetails.objects.filter(equipment=response.data["id"],
                                                                           is_deleted=False)
            contract_dict = {}
            for contract in contract_queryset:
                contract_dict['id'] = contract.id
                contract_dict['equipment'] = contract.equipment.id
                contract_dict['contractor'] = contract.contractor.id
            response.data['contract_details'] = contract_dict

        return response
class MachineriesListDetailsView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = CSPageNumberPagination
    queryset = PmsMachineries.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = MachineriesListDetailsSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('equipment_name', 'equipment_model_no', 'equipment_registration_no')
class MachineriesListWPDetailsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsMachineries.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = MachineriesListDetailsSerializer
    # filter_backends = (filters.SearchFilter,)
    # search_fields = ('equipment_name', 'equipment_model_no', 'equipment_registration_no')
class MachineriesListForReportView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsMachineries.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = MachineriesListDetailsSerializer
    def get(self, request, *args, **kwargs):
        response=list()
        todays_date = datetime.now()
        machineries_filter_list = PmsProjectsMachinaryMapping.objects.\
            filter(
            machinary_s_d_req__lte=todays_date,
            machinary_e_d_req__gte=todays_date
        )
        #print('machineries_filter_list_query',machineries_filter_list.query)
        #print('machineries_filter_list', machineries_filter_list)
        mech_list=list()
        for e_machine in machineries_filter_list:
            mech_list.append(e_machine.machinary.id)
        #print('mech_list',mech_list)
        mechine_details_list = PmsMachineries.objects.\
            filter(is_deleted=False,pk__in=mech_list)
        print('mechine_details_list',mechine_details_list)
        for e_mechine_details in mechine_details_list:
            response_d = {
                'id': e_mechine_details.id,
                'equipment_name': e_mechine_details.equipment_name,
                'equipment_category': e_mechine_details.equipment_category.id,
                'equipment_type': e_mechine_details.equipment_type,
                'owner_type': e_mechine_details.owner_type,
                'equipment_make': e_mechine_details.equipment_make,
                'equipment_model_no': e_mechine_details.equipment_model_no,
                'equipment_registration_no': e_mechine_details.equipment_registration_no,
                'equipment_chassis_serial_no': e_mechine_details.equipment_chassis_serial_no,
                'equipment_engine_serial_no': e_mechine_details.equipment_engine_serial_no,
                'equipment_power': e_mechine_details.equipment_power,
                'measurement_by': e_mechine_details.measurement_by,
                'measurement_quantity': e_mechine_details.measurement_quantity,
                'fuel_consumption': e_mechine_details.fuel_consumption,
                'remarks': e_mechine_details.remarks
            }
            PmsMachineriesWorkingCategoryde = PmsMachineriesWorkingCategory.objects.\
                filter(id=e_mechine_details.equipment_category.id,is_deleted=False)
            print('PmsMachineriesWorkingCategoryde',PmsMachineriesWorkingCategoryde)
            for e_PmsMachineriesWorkingCategoryde in PmsMachineriesWorkingCategoryde:
                w_c_details = { 'id':e_PmsMachineriesWorkingCategoryde.id,
                                'name':e_PmsMachineriesWorkingCategoryde.name,
                                'is_deleted': e_PmsMachineriesWorkingCategoryde.is_deleted,
                                }
            print('w_c_details',w_c_details)
            response_d['equipment_category_details'] = w_c_details
            PmsMachineriesDoc = PmsMachineriesDetailsDocument.objects.filter(
                equipment=e_mechine_details.id,is_deleted=False)
            #print('PmsMachineriesDoc', PmsMachineriesDoc)
            m_d_details_list=[]
            #request = self.context.get('request')
            for e_PmsMachineriesDoc in PmsMachineriesDoc:
                m_d_details = { 'id':e_PmsMachineriesDoc.id,
                                'name':e_PmsMachineriesDoc.document_name,
                                'document': request.build_absolute_uri(e_PmsMachineriesDoc.document.url),
                                'is_deleted': e_PmsMachineriesDoc.is_deleted,
                                }
                m_d_details_list.append(m_d_details)
            #print('m_d_details_list',m_d_details_list)
            response_d['document_details'] = m_d_details_list
            if e_mechine_details.owner_type == 1:
                # print('xyz',gfsdsdf)
                machinary_rented_details_queryset = PmsMachinaryRentedDetails.objects.filter(equipment=e_mechine_details.id,
                                                                                             is_deleted=False)
                #print('machinary_rented_details_queryset',machinary_rented_details_queryset)
                rental_details = dict()
                for machinary_rent in machinary_rented_details_queryset:
                    rental_details['id'] = machinary_rent.id
                    rental_details['equipment'] = machinary_rent.equipment.id
                    rental_details['vendor'] = machinary_rent.vendor.id
                    rental_details['rent_amount'] = machinary_rent.rent_amount
                    rental_details['type_of_rent'] = machinary_rent.type_of_rent.id
                if rental_details:
                    response_d["rental_details"] = rental_details
                    m_rented_details_vendor = PmsExternalUsers.objects.filter(
                        pk=machinary_rent.vendor.id,is_deleted=False)
                    print('m_rented_details_vendor',m_rented_details_vendor)
                    for e_m_rented_details_vendor in m_rented_details_vendor:
                        m_v_details = {'id': e_m_rented_details_vendor.id,
                                       'name': e_m_rented_details_vendor.name,
                                       'is_deleted': e_m_rented_details_vendor.is_deleted,
                                       }
                    response_d["rental_details"]['vendor_details']= m_v_details
            elif e_mechine_details.owner_type == 2:
                owner_queryset = PmsMachinaryOwnerDetails.objects.filter(equipment=e_mechine_details.id,
                                                                         is_deleted=False)
                #print('owner_queryset',owner_queryset)
                owner_dict = {}
                for owner in owner_queryset:
                    owner_dict['id'] = owner.id
                    owner_dict['equipment'] = owner.equipment.id
                    owner_dict['purchase_date'] = owner.purchase_date
                    owner_dict['price'] = owner.price
                    owner_dict['is_emi_available'] = owner.is_emi_available
                    if owner.is_emi_available:
                        emi_queryset = PmsMachinaryOwnerEmiDetails.objects.filter(equipment_owner_details=owner,
                                                                                  equipment=e_mechine_details.id,
                                                                                  is_deleted=False)
                        #print('emi_queryset',emi_queryset)
                        emi_dict = {}
                        for emi in emi_queryset:
                            emi_dict['id'] = emi.id
                            emi_dict['equipment'] = emi.equipment.id
                            emi_dict['equipment_owner_details'] = emi.equipment_owner_details.id
                            emi_dict['amount'] = emi.amount
                            emi_dict['start_date'] = emi.start_date
                            emi_dict['no_of_total_installment'] = emi.no_of_total_installment

                        if emi_dict:
                            owner_dict['owner_emi_details'] = emi_dict
                            #print('owner_dict',owner_dict)
                if owner_dict:
                    response_d['owner_details'] = owner_dict
            else:
                contract_queryset = PmsMachinaryContractDetails.objects.filter(equipment=e_mechine_details.id,
                                                                               is_deleted=False)
                contract_dict = {}
                for contract in contract_queryset:
                    contract_dict['id'] = contract.id
                    contract_dict['equipment'] = contract.equipment.id
                    contract_dict['contractor_id'] = contract.contractor.id
                    contract_dict['contractor'] = contract.contractor.name
                response_d['contract_details'] = contract_dict
            response.append(response_d)
        return Response(response)
class MachineriesListFilterForReportView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = CSPageNumberPagination
    queryset = PmsMachineries.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = MachineriesListDetailsSerializer
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter)
    filterset_fields = ('equipment_name','owner_type',)
    ordering_fields = '__all__'
    def list(self, request, *args, **kwargs):
        response = super(MachineriesListFilterForReportView, self).list(request, args, kwargs)
        for data in response.data['results']:
            PmsMachineriesWorkingCategoryde = PmsMachineriesWorkingCategory.objects.filter(
                id=data['equipment_category'],is_deleted=False)
            for e_PmsMachineriesWorkingCategoryde in PmsMachineriesWorkingCategoryde:
                w_c_details = { 'id':e_PmsMachineriesWorkingCategoryde.id,
                                'name':e_PmsMachineriesWorkingCategoryde.name,
                                'is_deleted': e_PmsMachineriesWorkingCategoryde.is_deleted,
                                }
            data['equipment_category_details'] = w_c_details
            PmsMachineriesDoc = PmsMachineriesDetailsDocument.objects.filter(
                equipment=data['id'],is_deleted=False)
            m_d_details_list=[]
            for e_PmsMachineriesDoc in PmsMachineriesDoc:
                m_d_details = { 'id':e_PmsMachineriesDoc.id,
                                'name':e_PmsMachineriesDoc.document_name,
                                'document': request.build_absolute_uri(e_PmsMachineriesDoc.document.url),
                                'is_deleted': e_PmsMachineriesDoc.is_deleted,
                                }
                m_d_details_list.append(m_d_details)
            data['document_details'] = m_d_details_list
            if data['owner_type'] == 1:
                machinary_rented_details_queryset = PmsMachinaryRentedDetails.objects.filter(
                    equipment=data['id'],is_deleted=False)
                #print('machinary_rented_details_queryset',machinary_rented_details_queryset)
                rental_details = dict()
                for machinary_rent in machinary_rented_details_queryset:
                    rental_details['id'] = machinary_rent.id
                    rental_details['equipment'] = machinary_rent.equipment.id
                    rental_details['vendor'] = machinary_rent.vendor.id
                    rental_details['rent_amount'] = machinary_rent.rent_amount
                    rental_details['type_of_rent'] = machinary_rent.type_of_rent.id
                if rental_details:
                    data["rental_details"] = rental_details
                    m_rented_details_vendor = PmsExternalUsers.objects.filter(
                        pk=machinary_rent.vendor.id,is_deleted=False)
                    #print('m_rented_details_vendor',m_rented_details_vendor)
                    for e_m_rented_details_vendor in m_rented_details_vendor:
                        m_v_details = {'id': e_m_rented_details_vendor.id,
                                       'name': e_m_rented_details_vendor.name,
                                       'is_deleted': e_m_rented_details_vendor.is_deleted,
                                       }
                    data["rental_details"]['vendor_details']= m_v_details
            elif data['owner_type'] == 2:
                owner_queryset = PmsMachinaryOwnerDetails.objects.filter(
                    equipment=data['id'],is_deleted=False)
                #print('owner_queryset',owner_queryset)
                owner_dict = {}
                for owner in owner_queryset:
                    owner_dict['id'] = owner.id
                    owner_dict['equipment'] = owner.equipment.id
                    owner_dict['purchase_date'] = owner.purchase_date
                    owner_dict['price'] = owner.price
                    owner_dict['is_emi_available'] = owner.is_emi_available
                    if owner.is_emi_available:
                        emi_queryset = PmsMachinaryOwnerEmiDetails.objects.filter(
                            equipment_owner_details=owner,
                              equipment=data['id'],
                              is_deleted=False
                        )
                        #print('emi_queryset',emi_queryset)
                        emi_dict = {}
                        for emi in emi_queryset:
                            emi_dict['id'] = emi.id
                            emi_dict['equipment'] = emi.equipment.id
                            emi_dict['equipment_owner_details'] = emi.equipment_owner_details.id
                            emi_dict['amount'] = emi.amount
                            emi_dict['start_date'] = emi.start_date
                            emi_dict['no_of_total_installment'] = emi.no_of_total_installment

                        if emi_dict:
                            data['owner_emi_details'] = emi_dict
                            #print('owner_dict',owner_dict)
                if owner_dict:
                    data['owner_details'] = owner_dict
            else:
                contract_queryset = PmsMachinaryContractDetails.objects.filter(
                    equipment=data['id'],is_deleted=False)
                contract_dict = {}
                for contract in contract_queryset:
                    contract_dict['id'] = contract.id
                    contract_dict['equipment'] = contract.equipment.id
                    contract_dict['contractor_id'] = contract.contractor.id
                    contract_dict['contractor'] = contract.contractor.name
                data['contract_details'] = contract_dict
        return response
class MachineriesDeleteView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsMachineries.objects.all()
    serializer_class = MachineriesDeleteSerializer

#::::::::::::::::: MECHINARY WORKING CATEGORY  :::::::::::::::#
class MachineriesWorkingCategoryAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsMachineriesWorkingCategory.objects.filter(is_deleted=False).order_by('-id')
    serializer_class= MachineriesWorkingCategoryAddSerializer
class MachineriesWorkingCategoryEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsMachineriesWorkingCategory.objects.all()
    serializer_class = MachineriesWorkingCategoryEditSerializer
class MachineriesWorkingCategoryDeleteView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsMachineriesWorkingCategory.objects.all()
    serializer_class = MachineriesWorkingCategoryDeleteSerializer

#::::::::::::::::: MECHINARY DETAILS DOCUMENT  :::::::::::::::#
class MachineriesDetailsDocumentAddView(generics.ListCreateAPIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [TokenAuthentication]
	queryset = PmsMachineriesDetailsDocument.objects.all()
	serializer_class = MachineriesDetailsDocumentAddSerializer
class MachineriesDetailsDocumentEditView(generics.RetrieveUpdateAPIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [TokenAuthentication]
	queryset = PmsMachineriesDetailsDocument.objects.all()
	serializer_class = MachineriesDetailsDocumentEditSerializer
class MachineriesDetailsDocumentDeleteView(generics.RetrieveUpdateAPIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [TokenAuthentication]
	queryset = PmsMachineriesDetailsDocument.objects.all()
	serializer_class = MachineriesDetailsDocumentDeleteSerializer
class MachineriesDetailsDocumentListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = MachineriesDetailsDocumentListSerializer
    def get_queryset(self):
        equipment_id = self.kwargs['equipment_id']
        queryset = PmsMachineriesDetailsDocument.objects.filter(equipment_id=equipment_id,is_deleted=False).order_by('-id')
        return queryset

#:::::::::::::::::  PMS External Users Type ::::::::::::::::::::#
class ExternalUsersTypeAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsExternalUsersType.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = ExternalUsersTypeAddSerializer
class ExternalUsersTypeEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsExternalUsersType.objects.all()
    serializer_class = ExternalUsersTypeEditSerializer
class ExternalUsersTypeDeleteView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsExternalUsersType.objects.all()
    serializer_class = ExternalUsersTypeDeleteSerializer

#:::::::::::::::::  PmsExternalUsers ::::::::::::::::::::#
class ExternalUsersAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsExternalUsers.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = ExternalUsersAddSerializer
class ExternalUsersEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsExternalUsers.objects.all()
    serializer_class = ExternalUsersEditSerializer
class ExternalUsersDeleteView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsExternalUsers.objects.all()
    serializer_class =  ExternalUsersDeleteSerializer
class ExternalUsersDocumentAddView(generics.ListCreateAPIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [TokenAuthentication]
	queryset = PmsExternalUsersDocument.objects.all()
	serializer_class = ExternalUsersDocumentAddSerializer
class ExternalUsersDocumentEditView(generics.RetrieveUpdateAPIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [TokenAuthentication]
	queryset = PmsExternalUsersDocument.objects.all()
	serializer_class = ExternalUsersDocumentEditSerializer
class ExternalUsersDocumentDeleteView(generics.RetrieveUpdateAPIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [TokenAuthentication]
	queryset = PmsExternalUsersDocument.objects.all()
	serializer_class = ExternalUsersDocumentDeleteSerializer
class ExternalUsersDocumentListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    # queryset = PmsExternalUsersDocument.objects.all()
    serializer_class = ExternalUsersDocumentListSerializer
    def get_queryset(self):
        external_user_id = self.kwargs['external_user_id']
        queryset = PmsExternalUsersDocument.objects.filter(external_user_id=external_user_id,is_deleted=False).order_by('-id')
        return queryset

#::::::::::::::: Pms Machinary Rented Type Master:::::::::::::::::::::#
class MachinaryRentedTypeMasterAddView(generics.ListCreateAPIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [TokenAuthentication]
	queryset = PmsMachinaryRentedTypeMaster.objects.filter(is_deleted=False).order_by('-id')
	serializer_class = MachinaryRentedTypeMasterAddSerializer
class MachinaryRentedTypeMasterEditView(generics.RetrieveUpdateAPIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [TokenAuthentication]
	queryset = PmsMachinaryRentedTypeMaster.objects.all()
	serializer_class = MachinaryRentedTypeMasterEditSerializer
class MachinaryRentedTypeMasterDeleteView(generics.RetrieveUpdateAPIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [TokenAuthentication]
	queryset = PmsMachinaryRentedTypeMaster.objects.all()
	serializer_class = MachinaryRentedTypeMasterDeleteSerializer

#::::::::::::::: PmsTenderTabDocuments :::::::::::::::::::::#
class TenderTabDocumentAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderTabDocuments.objects.all()
    serializer_class = TenderTabDocumentAddSerializer
class TenderTabDocumentEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderTabDocuments.objects.filter(status=True, is_deleted=False)
    serializer_class = TenderTabDocumentEditSerializer
class TenderTabDocumentDeleteView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = TenderTabDocumentDeleteSerializer
    queryset = PmsTenderTabDocuments.objects.all()

#:::::::::::::::PmsTenderTabDocumentsPrice:::::::::::::::::::::#
class TenderTabDocumentPriceAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderTabDocumentsPrice.objects.all()
    serializer_class = TenderTabDocumentPriceAddSerializer
class TenderTabDocumentPriceEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderTabDocumentsPrice.objects.filter(status=True, is_deleted=False)
    serializer_class = TenderTabDocumentPriceEditSerializer
class TenderTabDocumentPriceDeleteView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderTabDocumentsPrice.objects.all()
    serializer_class = TenderTabDocumentPriceDeleteSerializer

#::::::::::::: Pms Site Type Project Site Management ::::::::::::::::::::#
class SiteTypeProjectSiteManagementAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsSiteTypeProjectSiteManagement.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = SiteTypeProjectSiteManagementAddSerializer
    @response_modify_decorator
    def list(self, request, *args, **kwargs):
        return response
class SiteTypeProjectSiteManagementEditView(generics.RetrieveUpdateAPIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [TokenAuthentication]
	queryset = PmsSiteTypeProjectSiteManagement.objects.all()
	serializer_class = SiteTypeProjectSiteManagementEditSerializer
class SiteTypeProjectSiteManagementDeleteView(generics.RetrieveUpdateAPIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [TokenAuthentication]
	queryset = PmsSiteTypeProjectSiteManagement.objects.all()
	serializer_class = SiteTypeProjectSiteManagementDeleteSerializer

#::::::::::::::: Pms Site Project Site Management ::::::::::::::::::::#
class ProjectSiteManagementSiteAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsSiteProjectSiteManagement.objects.filter(is_deleted=False)
    serializer_class = ProjectSiteManagementSiteAddSerializer
    filter_backends = ( filters.SearchFilter,filters.OrderingFilter,)
    search_fields =('name','address','latitude','longitude','company_name',
                    'gst_no','geo_fencing_area','type__name')
    ordering = ('-id',)

    def list(self, request, *args, **kwargs):
        response = super(ProjectSiteManagementSiteAddView, self).list(request, args, kwargs)
        print('response: ', response.data)
        data_dict = {}
        data_dict['result'] = response.data
        if response.data:
            data_dict['request_status'] = 1
            data_dict['msg'] = settings.MSG_SUCCESS
        elif len(response.data)==0:
            data_dict['request_status'] = 1
            data_dict['msg'] =settings.MSG_NO_DATA
        else:
            data_dict['request_status'] = 0
            data_dict['msg'] = settings.MSG_ERROR

        response.data = data_dict
        return response
class ProjectSiteManagementSiteEditView(generics.RetrieveUpdateAPIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [TokenAuthentication]
	queryset = PmsSiteProjectSiteManagement.objects.all()
	serializer_class = ProjectSiteManagementSiteEditSerializer
class ProjectSiteManagementSiteDeleteView(generics.RetrieveUpdateAPIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [TokenAuthentication]
	queryset = PmsSiteProjectSiteManagement.objects.all()
	serializer_class = ProjectSiteManagementSiteDeleteSerializer
class ProjectSiteManagementSiteListWPView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsSiteProjectSiteManagement.objects.filter(is_deleted=False)
    serializer_class = ProjectSiteManagementSiteAddSerializer
    # filter_backends = ( filters.SearchFilter,filters.OrderingFilter,)
    # search_fields =('name','address','company_name','gst_no','geo_fencing_area','type__name')
    # ordering = ('-id',)

#:::::::::::: PROJECTS ::::::::::::::::::::::::::::#
class ProjectsAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsProjects.objects.all()
    serializer_class=ProjectsAddSerializer
class ProjectsListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    #pagination_class = CSPageNumberPagination
    queryset = PmsProjects.objects.filter(is_deleted=False).order_by('-id')
    serializer_class=ProjectsListSerializer
class ProjectsEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsProjects.objects.all()
    serializer_class = ProjectsEditSerializer
    def get(self, request, *args, **kwargs):
        response=dict()
        #print('kwargs',kwargs)
        project = PmsProjects.objects.filter(is_deleted=False,pk=kwargs['pk'])
        #print('project',project)
        for e_project in project:
            #print('e_project',e_project.id)
            response = {
                'id': int(e_project.id),
                'project_g_id':e_project.project_g_id,
                'name':e_project.name,
                'site_location': e_project.site_location.id,
                'start_date': e_project.start_date,
                'end_date': e_project.end_date,
                'updated_by': e_project.updated_by.username,
            }
        m_list = list()
        e_list = list()
        machinary_list = PmsProjectsMachinaryMapping.objects.filter(project=e_project.id,
                                                                    is_deleted=False)

        if machinary_list is None:
            m_list = []
        else:
            for e_machinary in machinary_list:
                m_list.append(
                    {'id': int(e_machinary.id),
                     'machinary': e_machinary.machinary.id,
                     'project': e_machinary.project.id,
                     'machinary_s_d_req': e_machinary.machinary_s_d_req,
                     'machinary_e_d_req': e_machinary.machinary_e_d_req
                     }
                )

        response['machinary_list'] = m_list
        employee_list = PmsProjectUserMapping.objects.filter(project=e_project.id, is_deleted=False)
        if employee_list is None:
            e_list=[]
        else:
            for e_l in employee_list:
                e_list.append(
                    {'id': int(e_l.id),
                     'user': e_l.user.id,
                     'project': e_l.project.id,
                     'start_date': e_l.start_date,
                     'expire_date': e_l.expire_date
                     }
                )
        response['employee_list'] = e_list
        #print('response',response)
        return Response(response)
class ProjectsDeleteView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsProjects.objects.all()
    serializer_class = ProjectsDeleteSerializer

#:::::::::::::::::::  Manpower :::::::::::::::::::::::::::#
class ManPowerListWOView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = TMasterModuleRole.objects.filter(mmr_user__isnull=False)
    serializer_class =UserModuleWiseListSerializer
    def get_queryset(self):
        module_id=self.kwargs['module_id']
        return self.queryset.filter(mmr_module_id=module_id)

    def get(self,request,*args,**kwargs):
        response = super(ManPowerListWOView, self).get(self, request, args, kwargs)
        print('response',response.data)
        module_id = self.kwargs['module_id']
        for data in response.data:
            if data['mmr_user']:
                #print('data:',data)
                employee_details = TCoreUserDetail.objects.filter(cu_user=data['mmr_user'])
                for employee in employee_details:
                    manpower_dict = {}
                    #print("employee: ", employee.cu_user_id)
                    manpower_dict['employee_id']=employee.cu_user_id
                    manpower_dict['employee_code'] = employee.cu_emp_code
                    name = employee.cu_user.first_name + ' ' +employee.cu_user.last_name
                    manpower_dict['employee_name']=name.strip()
                    manpower_dict['email_id']=employee.cu_user.email
                    manpower_dict['contact_no']=employee.cu_phone_no

                    project_details = PmsProjectUserMapping.objects.filter(user_id=employee.cu_user_id)
                    projects = []
                    for project in project_details:
                        project_data = {"id": project.project.id, "name": project.project.name}
                        projects.append(project_data)
                data['project'] = projects
                designation_details = TMasterModuleRole.objects.filter(
                    mmr_user=data['mmr_user'],mmr_module=module_id)
                #print('designation_details',designation_details)
                for designation in designation_details:
                    #print('designation',designation.mmr_group)
                    data['designation'] =designation.mmr_group.mmg_name
                data['mmr_user'] = manpower_dict
        return response
class ManPowerListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = CSPageNumberPagination
    queryset = TMasterModuleRole.objects.filter(mmr_user__isnull=False)
    serializer_class = UserModuleWiseListSerializer
    def get_queryset(self):
        module_id = self.kwargs['module_id']
        return self.queryset.filter(mmr_module_id=module_id)
    def get(self, request, *args, **kwargs):
        response = super(ManPowerListView, self).get(self, request, args, kwargs)
        print('response', response.data)
        module_id = self.kwargs['module_id']
        for data in response.data['results']:
            if data['mmr_user']:
                # print('data:',data)
                employee_details = TCoreUserDetail.objects.filter(cu_user=data['mmr_user'])
                for employee in employee_details:
                    manpower_dict = {}
                    # print("employee: ", employee.cu_user_id)
                    manpower_dict['employee_id'] = employee.cu_user_id
                    manpower_dict['employee_code'] = employee.cu_emp_code
                    name = employee.cu_user.first_name + ' ' + employee.cu_user.last_name
                    manpower_dict['employee_name'] = name.strip()
                    manpower_dict['email_id'] = employee.cu_user.email
                    manpower_dict['contact_no'] = employee.cu_phone_no

                    project_details = PmsProjectUserMapping.objects.filter(user_id=employee.cu_user_id)
                    projects = []
                    for project in project_details:
                        project_data = {"id": project.project.id, "name": project.project.name}
                        projects.append(project_data)
                data['project'] = projects
                designation_details = TMasterModuleRole.objects.filter(
                    mmr_user=data['mmr_user'], mmr_module=module_id)
                # print('designation_details',designation_details)
                for designation in designation_details:
                    # print('designation',designation.mmr_group)
                    data['designation'] = designation.mmr_group.mmg_name
                data['mmr_user'] = manpower_dict
        return response

#:::::::::::: MECHINARY REPORTS ::::::::::::::::::::::::::::#
class MachineriesReportAddView(generics.ListCreateAPIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [TokenAuthentication]
	queryset = PmsProjectsMachinaryReport.objects.all()
	serializer_class = MachineriesReportAddSerializer
class MachineriesReportEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsProjectsMachinaryReport.objects.all()
    serializer_class = MachineriesReportEditSerializer
