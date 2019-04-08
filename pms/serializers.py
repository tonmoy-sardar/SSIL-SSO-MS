from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from pms.models import *
from django.contrib.auth.models import *
import time
from django.db import transaction, IntegrityError
from drf_extra_fields.fields import Base64ImageField
import os
from rest_framework.exceptions import APIException
import datetime
from core.models import TCoreUnit


#:::::::::: TENDER AND TENDER DOCUMENTS  ::::::::#
class TenderEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = PmsTenders
        fields = ('id','updated_by','tender_final_date',
                  'tender_opened_on','tender_added_by','tender_received_on',
                  'tender_aasigned_to')
class TenderDocumentAddSerializer(serializers.ModelSerializer):
    tender_document = serializers.FileField(required=False)
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    tender_documents = serializers.ListField(required=False)
    status = serializers.BooleanField(default=True)
    class Meta:
        model = PmsTenderDocuments
        fields = ('id','tender','document_name','tender_document',
                  'created_by','owned_by','status','tender_documents')
class TenderDeleteSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = PmsTenders
        fields = ("id",'updated_by','status','is_deleted')

    def update(self, instance, validated_data):
        try:
            with transaction.atomic():
                instance.updated_by = validated_data.get('updated_by')
                instance.is_deleted = True
                instance.status = False
                instance.save()
                pmsTenderDocuments = PmsTenderDocuments.objects.get(tender=instance.id)
                pmsTenderDocuments.status = False
                pmsTenderDocuments.is_deleted = True
                pmsTenderDocuments.save()
                return instance
        except Exception as e:
            raise e
class TenderDocsEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = PmsTenderDocuments
        fields = ('id','document_name','updated_by')
class TenderDocumentDeleteSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = PmsTenderDocuments
        fields = ("id",'updated_by','status','is_deleted')

    def update(self, instance, validated_data):
        try:
            with transaction.atomic():
                instance.updated_by = validated_data.get('updated_by')
                instance.is_deleted = True
                instance.status = False
                instance.save()
                return instance
        except Exception as e:
            raise e
class TendersAddSerializer(serializers.ModelSerializer):
    tender_g_id = serializers.CharField(required=False)
    created_by=serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by=serializers.CharField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)
    class Meta:
        model = PmsTenders
        fields = ('id','tender_g_id',"tender_final_date","tender_opened_on",
                  "tender_added_by",'tender_received_on','tender_aasigned_to',
                  'created_by','owned_by','status')
    def create(self, validated_data):
        try:
            tender_id = "T" + str(int(time.time()))
            #print('tender_id', tender_id)
            created_by = validated_data.get('created_by')
            #print('created_by',created_by)
            owned_by = validated_data.get('owned_by')
            with transaction.atomic():
                tender_save_id = PmsTenders.objects.create(
                        tender_g_id=tender_id,
                        tender_final_date=validated_data.get('tender_final_date'),
                        tender_opened_on=validated_data.get('tender_opened_on'),
                        tender_added_by=validated_data.get('tender_added_by'),
                        tender_received_on=validated_data.get('tender_received_on'),
                        tender_aasigned_to=validated_data.get('tender_aasigned_to'),
                        created_by=created_by,
                        owned_by=owned_by
                       )
                response_data={
                    'id':tender_save_id.id,
                    'tender_g_id':tender_save_id.tender_g_id,
                    'tender_final_date': tender_save_id.tender_final_date,
                    'tender_opened_on': tender_save_id.tender_opened_on,
                    'tender_added_by': tender_save_id.tender_added_by,
                    'tender_received_on': tender_save_id.tender_received_on,
                    'tender_aasigned_to': tender_save_id.tender_aasigned_to,
                    'created_by':tender_save_id.created_by,
                    'owned_by':tender_save_id.owned_by,
                    }
                return response_data

        except Exception as e:
            raise e

#:::::::::: TENDER  BIDDER TYPE :::::::::::::::#
class VendorsAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)
    class Meta:
        model=PmsTenderVendors
        fields='__all__'
class VendorsMappingSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    owned_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    tender_bidder_type = serializers.CharField(required=False)
    status = serializers.HiddenField(default=1)
    tender_vendor = VendorsAddSerializer()
    class Meta:
        model=PmsTenderBidderTypeVendorMapping
        fields=('id','tender_bidder_type','tender_vendor',
                'status','created_by','owned_by')
class TendorBidderTypeAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)
    vendors = serializers.ListField(required=False)
    type_of_partner = serializers.IntegerField(required=False)
    class Meta:
        model=PmsTenderBidderType
        fields=('id','tender','bidder_type','type_of_partner','responsibility',
                'profit_sharing_ratio_actual_amount',
                'profit_sharing_ratio_tender_specific_amount','created_by',
                'owned_by','vendors','status')
    def create(self, validated_data):
        try:
            tender_bidder_type_vendor_mapping_list=[]
            with transaction.atomic():
                if validated_data.get('bidder_type') == 'individual':
                    tender_bidder_type = PmsTenderBidderType.objects.create(tender=validated_data.get('tender'),
                                                                            bidder_type=validated_data.get(
                                                                                'bidder_type'),
                                                                            responsibility=validated_data.get(
                                                                                'responsibility'),
                                                                            status=validated_data.get('status'),
                                                                            created_by=validated_data.get('created_by'),
                                                                            owned_by=validated_data.get('owned_by')

                                                                            )
                    response = {
                        'id': tender_bidder_type.id,
                        'tender': tender_bidder_type.tender,
                        'bidder_type': tender_bidder_type.bidder_type,
                        'created_by': tender_bidder_type.created_by,
                        'owned_by': tender_bidder_type.owned_by,
                    }
                    return response
                else:
                    tender_bidder_type=PmsTenderBidderType.objects.create(
                        tender=validated_data.get('tender'),
                        bidder_type=validated_data.get('bidder_type'),
                        type_of_partner=validated_data.get('type_of_partner'),
                        responsibility=validated_data.get('responsibility'),
                        profit_sharing_ratio_actual_amount=validated_data.get('profit_sharing_ratio_actual_amount'),
                        profit_sharing_ratio_tender_specific_amount=validated_data.get('profit_sharing_ratio_tender_specific_amount'),
                        status = validated_data.get('status'),
                        created_by=validated_data.get('created_by'),
                        owned_by=validated_data.get('owned_by'))

                    for vendor in validated_data.get('vendors'):
                        print('vendor',vendor)
                        request_dict = {
                                    "tender_bidder_type_id": str(tender_bidder_type),
                                    "tender_vendor_id": int(vendor),
                                    "status": True,
                                    "created_by": validated_data.get('created_by'),
                                    "owned_by": validated_data.get('owned_by')
                                   }
                        tender_bidder_type_vendor_m, created=PmsTenderBidderTypeVendorMapping.objects.get_or_create(**request_dict)
                        tender_bidder_type_vendor_mapping_list.append({
                                "id" : tender_bidder_type_vendor_m.tender_vendor.id,
                                "name": tender_bidder_type_vendor_m.tender_vendor.name
                            })
                    #print('tender_bidder_type_vendor_mapping_list',tender_bidder_type_vendor_mapping_list)
                    response={
                        'id':tender_bidder_type.id,
                        'tender':tender_bidder_type.tender,
                        'bidder_type':tender_bidder_type.bidder_type,
                        'type_of_partner':tender_bidder_type.type_of_partner,
                        'responsibility':tender_bidder_type.responsibility,
                        'profit_sharing_ratio_actual_amount':tender_bidder_type.profit_sharing_ratio_actual_amount,
                        'profit_sharing_ratio_tender_specific_amount':tender_bidder_type.profit_sharing_ratio_tender_specific_amount,
                        'created_by':tender_bidder_type.created_by,
                        'owned_by':tender_bidder_type.owned_by,
                        'vendors':validated_data.get('vendors')

                    }
                    return response
        except Exception as e:
            raise APIException({'request_status': 0, 'msg': e})
class TendorBidderTypeEditSerializer(serializers.ModelSerializer):
    updated_by=serializers.CharField(default=serializers.CurrentUserDefault())
    vendors = serializers.ListField(required=True)
    class Meta:
        model=PmsTenderBidderType
        fields = ( 'id', 'bidder_type','type_of_partner', 'responsibility',
                   'profit_sharing_ratio_actual_amount',
                   'profit_sharing_ratio_tender_specific_amount', 'updated_by','vendors')

    def update(self, instance, validated_data):
        try:
            tender_bidder_type_vendor_mapping_list = []
            with transaction.atomic():
                instance.bidder_type = validated_data.get('bidder_type', instance.bidder_type)
                instance.type_of_partner=validated_data.get('type_of_partner',instance.type_of_partner)
                print('instance.type_of_partner',instance.type_of_partner)
                instance.responsibility=validated_data.get('responsibility',instance.responsibility)
                instance.profit_sharing_ratio_actual_amount=validated_data.get('profit_sharing_ratio_actual_amount',instance.profit_sharing_ratio_actual_amount)
                instance.profit_sharing_ratio_tender_specific_amount=validated_data.get('profit_sharing_ratio_tender_specific_amount',instance.profit_sharing_ratio_tender_specific_amount)
                instance.updated_by=validated_data.get('updated_by',instance.updated_by)
                instance.save()

                xyz=PmsTenderBidderTypeVendorMapping.objects.filter(tender_bidder_type_id=instance.id).delete()
                print('xyz',xyz)

                for vendor in validated_data.get('vendors'):
                    request_dict = {
                        "tender_bidder_type_id": str(instance.id),
                        "tender_vendor_id": vendor['tender_vendor_id'],
                        "status": True,
                        "created_by": validated_data.get('created_by'),
                        "owned_by": validated_data.get('owned_by')
                    }
                    tender_bidder_type_vendor_m, created = PmsTenderBidderTypeVendorMapping.objects.get_or_create(
                        **request_dict)
                    tender_bidder_type_vendor_mapping_list.append({
                        "id": tender_bidder_type_vendor_m.tender_vendor.id,
                        "name": tender_bidder_type_vendor_m.tender_vendor.name
                    })

                response = {
                    'id': instance.id,
                    'tender': instance.tender,
                    'bidder_type': instance.bidder_type,
                    'type_of_partner':  instance.type_of_partner,
                    'responsibility': instance.responsibility,
                    'profit_sharing_ratio_actual_amount':  instance.profit_sharing_ratio_actual_amount,
                    'profit_sharing_ratio_tender_specific_amount':  instance.profit_sharing_ratio_tender_specific_amount,
                    'updated_by': instance.updated_by,
                    'vendors': tender_bidder_type_vendor_mapping_list

                }
                return response
        except Exception as e:
            raise e
class TendorBidderTypeDeleteSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model=PmsTenderBidderType
        fields=('id','type_of_partner', 'responsibility', 'profit_sharing_ratio_actual_amount',
        'profit_sharing_ratio_tender_specific_amount','status','is_deleted','updated_by','created_by','owned_by')

    def update(self, instance, validated_data):
        with transaction.atomic():
            instance.status=False
            instance.is_deleted=True
            instance.save()

            PmsTenderBidderTypeVendorMapping.objects.filter(tender_bidder_type_id=instance.id).update(status=False,is_deleted=True)

            response_data={ 'id':instance.id,
                            'tender': instance.tender,
                            'bidder_type': instance.bidder_type,
                            'type_of_partner': instance.type_of_partner,
                            'responsibility': instance.responsibility,
                            'profit_sharing_ratio_actual_amount': instance.profit_sharing_ratio_actual_amount,
                            'profit_sharing_ratio_tender_specific_amount': instance.profit_sharing_ratio_tender_specific_amount,
                            'created_by':instance.created_by,
                            'updated_by': instance.updated_by,
                            'owned_by': instance.owned_by,
                            'status':instance.status,
                            'is_deleted':instance.is_deleted
            }

            return  response_data


#:::::::::: TENDER  ELIGIBILITY :::::::::::::::#
class PmsTenderEligibilityAddSerializer(serializers.ModelSerializer):
    """Eligibility is added with the required parameters,
     using 2 table 'PmsTenderEligibility' and 'PmsTenderEligibilityFieldsByType'
     uniquely added on 'PmsTenderEligibility',
     transaction is exist,
     APIException is used. """
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    eligibility_type = serializers.CharField(required=True)
    eligibility_status = serializers.BooleanField(required=False)
    eligibility_fields = serializers.ListField(required=True)
    tender_id = serializers.IntegerField(required=True)
    class Meta:
        model = PmsTenderEligibility
        fields = ('id', 'tender_id', 'eligibility_type', 'eligibility_status', 'eligibility_fields', 'created_by')

    def create(self, validated_data):
        self.eligibility_status = True
        try:
            fields_result_list = list()
            current_user = validated_data.get('created_by')
            tender_id = validated_data.pop('tender_id') if "tender_id" in validated_data else 0
            eligibility_type = validated_data.pop('eligibility_type') if "eligibility_type" in validated_data else ""
            ineligibility_reason = validated_data.pop(
                'ineligibility_reason') if "ineligibility_reason" in validated_data else ""
            eligibility_fields = validated_data.pop('eligibility_fields')
            with transaction.atomic():
                if tender_id:
                    tender_eligibility_dict = {}
                    tender_eligibility_dict['tender_id'] = tender_id
                    tender_eligibility_dict['type'] = eligibility_type
                    tender_eligibility_dict['created_by'] = current_user
                    tender_eligibility_dict['owned_by'] = current_user

                    add_tender_eligibility,  created= PmsTenderEligibility.objects.get_or_create(**tender_eligibility_dict)
                    PmsTenderEligibilityFieldsByType.objects.filter(tender_id=tender_id,
                                                                    tender_eligibility_id=add_tender_eligibility.id).delete()
                    for fields_data in eligibility_fields:
                        print("fields_data: ", fields_data)
                        fields_data['tender_id'] = tender_id
                        fields_data['tender_eligibility'] = add_tender_eligibility
                        fields_data['created_by'] = current_user
                        fields_data['owned_by'] = current_user
                        print("eligibility_status: ", self.eligibility_status)
                        if not fields_data['eligible']:
                            self.eligibility_status = False



                        add_tender_eligibilityfields_by_type = PmsTenderEligibilityFieldsByType.objects.create(**fields_data)
                        added_fields = {"id": add_tender_eligibilityfields_by_type.id,
                                        "tender_id": add_tender_eligibilityfields_by_type.tender_id,
                                        "tender_eligibility_id": add_tender_eligibilityfields_by_type.tender_eligibility_id,
                                        "field_label": add_tender_eligibilityfields_by_type.field_label,
                                        "field_value": add_tender_eligibilityfields_by_type.field_value,
                                        "eligible": add_tender_eligibilityfields_by_type.eligible
                                        }
                        fields_result_list.append(added_fields)
                    if not self.eligibility_status:
                        PmsTenderEligibility.objects.filter(pk=add_tender_eligibility.id).update(
                            eligibility_status=False)
                    else:
                        PmsTenderEligibility.objects.filter(pk=add_tender_eligibility.id).update(
                            eligibility_status=True)
                    result_dict = {
                        "id": add_tender_eligibility.id,
                       "tender_id": add_tender_eligibility.tender.id,
                        "eligibility_type": add_tender_eligibility.type,
                        "eligibility_status": self.eligibility_status,
                       "eligibility_fields": fields_result_list
                                   }
            return result_dict
        except Exception as e:
            print("error: ", e)
            raise APIException({'request_status': 0, 'msg': e})
class PmsTenderEligibilityFieldsByTypeEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = PmsTenderEligibilityFieldsByType
        fields = ("id", "tender", "tender_eligibility", "field_label", "field_value", "eligible", "updated_by")
class PmsTenderNotEligibilityReasonAddSerializer(serializers.ModelSerializer):
    updated_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = PmsTenderEligibility
        fields = ("id", "tender", "ineligibility_reason",
                  "eligibility_status", "updated_by")

    def update(self, instance, validated_data):
        instance.ineligibility_reason = validated_data.get("ineligibility_reason",instance.ineligibility_reason)
        instance.save()
        return instance

#::::::::::::::: TENDER SURVEY SITE PHOTOS:::::::::::::::#
class TenderSurveySitePhotosAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)
    class Meta:
        model=PmsTenderSurveySitePhotos
        fields=('id','tender','latitude','longitude','address','additional_notes',
                'document','document_name','status','created_by','owned_by')
    def create(self, validated_data):
        try:
            survey_site_photos=PmsTenderSurveySitePhotos.objects.create(**validated_data)
            response_data={
                'id':survey_site_photos.id,
                'tender':survey_site_photos.tender,
                'latitude':survey_site_photos.latitude,
                'longitude':survey_site_photos.longitude,
                'address':survey_site_photos.address,
                'additional_notes':survey_site_photos.additional_notes,
                'document':survey_site_photos.document,
                'document_name': survey_site_photos.document_name,
                'status':survey_site_photos.status,
                'created_by':survey_site_photos.created_by,
                'owned_by':survey_site_photos.owned_by

            }
            return response_data
        except Exception as e:
            raise e
class TenderSurveySitePhotosEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model=PmsTenderSurveySitePhotos
        fields=('id','tender','latitude','longitude','address','additional_notes',
                'document','document_name','updated_by')
    def update(self, instance, validated_data):
        try:
            with transaction.atomic():
                instance.latitude=validated_data.get('latitude',instance.latitude)
                instance.longitude=validated_data.get('longitude',instance.longitude)
                instance.address=validated_data.get('address',instance.address)
                instance.additional_notes=validated_data.get('additional_notes',instance.additional_notes)
                instance.updated_by=validated_data.get('updated_by',instance.updated_by)
                instance.document_name=validated_data.get('document_name',instance.document_name)
                existing_image='./media/' + str(instance.document)
                if validated_data.get('document'):
                    if os.path.isfile(existing_image):
                        os.remove(existing_image)
                    instance.document = validated_data.get('document', instance.document)
                instance.save()
                return instance
        except Exception as e:
            raise APIException({'request_status': 0, 'msg': e})
class TenderSurveySitePhotosListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PmsTenderSurveySitePhotos
        fields = '__all__'
class TenderSurveySitePhotosDeleteSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = PmsTenderSurveySitePhotos
        fields = '__all__'
    def update(self, instance, validated_data):
        try:
            with transaction.atomic():
                instance.status = False
                instance.is_deleted = True
                instance.save()
                return instance
        except Exception as e:
            raise APIException({'request_status': 0, 'msg': e})

#::::::::::::::: TENDER SURVEY COORDINATE :::::::::::::::#
class TenderSurveyLocationAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)
    class Meta:
        model=PmsTenderSurveyCoordinatesSiteCoordinate
        fields=('id','tender','name','latitude','longitude','address','status',
                'created_by','owned_by')
    def create(self, validated_data):
        try:
            location_request=PmsTenderSurveyCoordinatesSiteCoordinate.objects.create(**validated_data)
            response_data={
                'id':location_request.id,
                'tender':location_request.tender,
                'name': location_request.name,
                'latitude':location_request.latitude,
                'longitude':location_request.longitude,
                'address':location_request.address,
                'status':location_request.status,
                'created_by':location_request.created_by,
                'owned_by':location_request.owned_by
            }
            return response_data
        except Exception as e:
            raise APIException({'request_status': 0, 'msg': e})
class TenderSurveyLocationListSerializer(serializers.ModelSerializer):
    class Meta:
        model=PmsTenderSurveyCoordinatesSiteCoordinate
        fields=('id','tender','name','latitude','longitude','address',
                'status','created_by','owned_by')
class TenderSurveyLocationEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model=PmsTenderSurveyCoordinatesSiteCoordinate
        fields=('id','tender','name','latitude','longitude','address','updated_by')
class TenderSurveyLocationDeleteSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = PmsTenderSurveyCoordinatesSiteCoordinate
        fields = '__all__'
    def update(self, instance, validated_data):
        try:
            with transaction.atomic():
                instance.status = False
                instance.is_deleted = True
                instance.save()
                response_data = {'id': instance.id,
                                 'tender': instance.tender,
                                 'name':instance.name,
                                 'latitude': instance.latitude,
                                 'longitude': instance.longitude,
                                 'address': instance.address,
                                 'created_by': instance.created_by,
                                 'updated_by': instance.updated_by,
                                 'owned_by': instance.owned_by,
                                 'status': instance.status,
                                 'is_deleted': instance.is_deleted
                                 }
                return response_data
        except Exception as e:
            raise APIException({'request_status': 0, 'msg': e})
class TenderSurveyCOSupplierListSerializer(serializers.ModelSerializer):
    survey_co_ordinate_supplier_document=serializers.SerializerMethodField(required=False)
    def get_survey_co_ordinate_supplier_document(self, PmsTenderSurveyCoordinatesSuppliers):
        document = PmsTenderSurveyCoordinatesSuppliersDocument.objects.filter(coordinate_supplier=PmsTenderSurveyCoordinatesSuppliers.id, is_deleted=False)
        request = self.context.get('request')
        response_list = []
        for each_document in document:
            file_url = request.build_absolute_uri(each_document.document.url)
            owned_by = str(each_document.owned_by) if each_document.owned_by else ''
            created_by = str(each_document.created_by) if each_document.created_by else ''
            each_data = {
                "id": int(each_document.id),
                "coordinate_supplier": each_document.coordinate_supplier.id,
                "document_name": each_document.document_name,
                "document": file_url,
                "created_by": created_by,
                "owned_by": owned_by
            }
            response_list.append(each_data)
        return response_list
    class Meta:
        model=PmsTenderSurveyCoordinatesSuppliers
        fields=('id','tender','type','tender_survey_material','supplier_name','contact',
                'latitude','longitude','address','status',
                'created_by','owned_by','updated_by','survey_co_ordinate_supplier_document')


class TenderSurveyCOSupplierAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)
    class Meta:
        model=PmsTenderSurveyCoordinatesSuppliers
        fields=('id','tender','type','tender_survey_material','supplier_name','contact',
                'latitude','longitude','address','status',
                'created_by','owned_by')
class TenderSurveyCOSupplierEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model=PmsTenderSurveyCoordinatesSuppliers
        fields=('id','tender','type','tender_survey_material','supplier_name','contact',
                'latitude','longitude','address','status',
                'created_by','owned_by','updated_by')
class TenderSurveyCOSupplierDeleteSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = PmsTenderSurveyCoordinatesSuppliers
        fields = '__all__'
    def update(self, instance, validated_data):
        try:
            with transaction.atomic():
                instance.status = False
                instance.is_deleted = True
                instance.save()
                return instance
        except Exception as e:
            raise APIException({'request_status': 0, 'msg': e})
class TenderSurveyCOSupplierDocumentAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)
    class Meta:
        model = PmsTenderSurveyCoordinatesSuppliersDocument
        fields = ('id', 'coordinate_supplier', 'document_name', 'document',
                  'status', 'created_by', 'owned_by')
class TenderSurveyCOSupplierDocumentEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PmsTenderSurveyCoordinatesSuppliersDocument
        fields = ('id', 'coordinate_supplier', 'document_name',
                  'updated_by',)
class TenderSurveyCOSupplierDocumentDeleteSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PmsTenderSurveyCoordinatesSuppliersDocument
        fields = '__all__'

        def update(self, instance, validated_data):
            instance.status = False
            instance.is_deleted = True
            instance.save()
            return instance

#::::::::::: TENDER SURVEY RESOURCE ::::::::::::::::::::#
class TenderSurveyMaterialsAddSerializer(serializers.ModelSerializer):
    status=serializers.BooleanField(default=True)
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model=PmsTenderSurveyMaterials
        fields=('id','name','tender','unit','status','created_by','owned_by')
class TenderSurveyMaterialsEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    unit_name = serializers.SerializerMethodField(required=False)
    def get_unit_name(self, PmsTenderSurveyMaterials):
        return TCoreUnit.objects.only('c_name').get(pk=PmsTenderSurveyMaterials.unit.id).c_name
    class Meta:
        model=PmsTenderSurveyMaterials
        fields=('id','name','unit','unit_name','tender','updated_by',)
class TenderSurveyMaterialsDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model=PmsTenderSurveyMaterials
        fields='__all__'
    def update(self, instance, validated_data):
        instance.status = False
        instance.is_deleted = True
        instance.save()
        response_data = {'id': instance.id,
                         'name': instance.name,
                         'unit': instance.unit,
                         'created_by': instance.created_by,
                         'updated_by': instance.updated_by,
                         'owned_by': instance.owned_by,
                         'status': instance.status,
                         'is_deleted': instance.is_deleted
                         }

        return response_data
class TenderSurveyMaterialsListSerializer(serializers.ModelSerializer):
    unit_name = serializers.SerializerMethodField(required=False)
    def get_unit_name(self, PmsTenderSurveyMaterials):
        return TCoreUnit.objects.only('c_name').get(pk=PmsTenderSurveyMaterials.unit.id).c_name
    class Meta:
        model = PmsTenderSurveyMaterials
        fields = ('id', 'name', 'tender', 'unit','unit_name','status', 'created_by', 'owned_by')

#::::::::::: TENDER SURVEY RESOURCE METERIAL SUPPLIERS ::::::::::::::::::::#
class TenderSurveyResourceMaterialAddSerializer(serializers.ModelSerializer):
    status = serializers.BooleanField(default=True)
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = PmsTenderSurveyResourceMaterial
        fields = ('id','tender','tender_survey_material','supplier_name','rate',
                  'latitude','longitude',
                  'address','status','created_by','owned_by')
class TenderSurveyResourceMaterialEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = PmsTenderSurveyResourceMaterial
        fields = ('id','tender_survey_material','supplier_name','rate','latitude','longitude',
                  'address','updated_by')
class TenderSurveyResourceMaterialDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PmsTenderSurveyResourceMaterial
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.status = False
        instance.is_deleted = True
        instance.save()

        return instance
class TenderSurveyResourceMaterialListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PmsTenderSurveyResourceMaterial
        fields = '__all__'
class TenderSurveyResourceMaterialDocumentAddSerializer(serializers.ModelSerializer):
    status = serializers.BooleanField(default=True)
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PmsTenderSurveyResourceMaterialDocument
        fields = ('id', 'survey_resource_material', 'document_name', 'document',
                  'status', 'created_by', 'owned_by')
class TenderSurveyResourceMaterialDocumentEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PmsTenderSurveyResourceMaterialDocument
        fields = ('id', 'survey_resource_material', 'document_name',
                  'updated_by')
class TenderSurveyResourceMaterialDocumentDeleteSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PmsTenderSurveyResourceMaterialDocument
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.updated_by = validated_data.get('updated_by')
        instance.status = False
        instance.is_deleted = True
        instance.save()
        return instance

#:::::::::: TENDER SURVEY RESOURCE ESTABLISHMENT :::::::::::#
class TenderSurveyResourceEstablishmentAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PmsTenderSurveyResourceEstablishment
        fields = (
        'id', 'tender', 'name', 'details', 'latitude', 'longitude', 'address', 'status', 'created_by', 'owned_by')
class TenderSurveyResourceEstablishmentEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PmsTenderSurveyResourceEstablishment
        fields = ('id', 'tender', 'name', 'details', 'latitude', 'longitude', 'address', 'status', 'updated_by')
class TenderSurveyResourceEstablishmentDeleteSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PmsTenderSurveyResourceEstablishment
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.status = False
        instance.is_deleted = True
        instance.updated_by = validated_data.get('updated_by')
        instance.save()
        return instance
class TenderSurveyResourceEstablishmentDocumentAddSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    owned_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)

    class Meta:
        model = PmsTenderSurveyDocument
        fields = ("id", "tender", "module_id", "document_name", "document", "created_by", "owned_by", 'status')

    def create(self, validated_data):
        resource_establishment_data = PmsTenderSurveyDocument.objects.create(**validated_data,
                                                                             model_class="PmsTenderSurveyResourceEstablishment")

        return resource_establishment_data
class TenderSurveyResourceEstablishmentDocumentEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PmsTenderSurveyDocument
        fields = ("id", "module_id", "document_name", "document", "updated_by")

    def update(self, instance, validated_data):
        instance.module_id = validated_data.get('module_id')
        instance.document_name = validated_data.get('document_name')
        instance.updated_by = validated_data.get('updated_by')
        existing_image = './media/' + str(instance.document)
        if validated_data.get('document'):
            if os.path.isfile(existing_image):
                os.remove(existing_image)
            instance.document = validated_data.get('document')
        instance.save()
        return instance
class TenderSurveyResourceEstablishmentDocumentDeleteSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PmsTenderSurveyDocument
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.status = False
        print('   instance.status ', instance.status)
        instance.updated_by = validated_data.get('updated_by')
        instance.is_deleted = True
        instance.save()
        return instance

#:::: TENDER SURVEY RESOURCE HYDROLOGICAL :::::::#
class TenderSurveyResourceHydrologicalAddSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    owned_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)
    class Meta:
        model = PmsTenderSurveyResourceHydrological
        fields = ("id", 'tender', "name", 'details', 'latitude', 'longitude', 'address', "created_by",
                  "owned_by", 'status')
class TenderSurveyResourceHydrologicalEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PmsTenderSurveyResourceHydrological
        fields = ("id","name", 'details', 'latitude', 'longitude', 'address', "updated_by"
                  )
class TenderSurveyResourceHydrologicalDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PmsTenderSurveyResourceHydrological
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.status = False
        instance.is_deleted = True
        instance.save()
        return instance
class TenderSurveyResourceHydrologicalDocumentAddSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    owned_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)
    class Meta:
        model = PmsTenderSurveyDocument
        fields = ("id", "tender", "module_id", "document_name",
                  "document", "created_by", "owned_by",'status')

    def create(self, validated_data):
        survey_document_data = PmsTenderSurveyDocument.objects.create(**validated_data,
                                                                      model_class="PmsTenderSurveyResourceHydrological")
        return survey_document_data
class TenderSurveyResourceHydrologicalDocumentEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PmsTenderSurveyDocument
        fields = ("id", "module_id", "document_name", "document", "updated_by")

    def update(self, instance, validated_data):
        instance.module_id = validated_data.get('module_id')
        instance.document_name = validated_data.get('document_name')
        instance.updated_by = validated_data.get('updated_by')
        existing_image = './media/' + str(instance.document)
        if validated_data.get('document'):
            if os.path.isfile(existing_image):
                os.remove(existing_image)
            instance.document = validated_data.get('document')
        instance.save()
        return instance
class TenderSurveyResourceHydrologicalDocumentDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PmsTenderSurveyDocument
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.status = False
        instance.is_deleted = True
        instance.save()
        return instance

#:::: TENDER SURVEY RESOURCE CONTRACTORS / VENDORS :::::::#
class TenderSurveyResourceContractorsOVendorsContractorAddSerializer(serializers.ModelSerializer):
    status = serializers.BooleanField(default=True)
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = PmsTenderSurveyResourceContractorsOVendorsContractor
        fields = ('id', 'tender','name','details','latitude','longitude',
                  'address', 'status', 'created_by','owned_by')
class TenderSurveyResourceContractorsOVendorsContractorEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = PmsTenderSurveyResourceContractorsOVendorsContractor
        fields = ('id','name','details','latitude','longitude','address','updated_by')
class TenderSurveyResourceContractorsOVendorsContractorDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PmsTenderSurveyResourceContractorsOVendorsContractor
        fields = '__all__'
    def update(self, instance, validated_data):
        instance.status = False
        instance.is_deleted = True
        instance.save()

        return instance
class TenderSurveyResourceContractorsOVendorsContractorDocumentAddSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    owned_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = PmsTenderSurveyDocument
        fields = ("id", "tender", "module_id", "document_name", "document",
                  "created_by", "owned_by")
    def create(self, validated_data):
        survey_document_data = PmsTenderSurveyDocument.objects.create(
            **validated_data,model_class="PmsTenderSurveyResourceContractorsOVendorsContractor")
        return survey_document_data
class TenderSurveyResourceContractorsOVendorsContractorDocumentEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = PmsTenderSurveyDocument
        fields = ("id", "module_id", "document_name", "document","updated_by")
    def update(self, instance, validated_data):
        instance.module_id=validated_data.get('module_id')
        instance.document_name=validated_data.get('document_name')
        instance.updated_by = validated_data.get('updated_by')
        existing_image = './media/' + str(instance.document)
        if validated_data.get('document'):
            if os.path.isfile(existing_image):
                os.remove(existing_image)
            instance.document = validated_data.get('document')
        instance.save()
        return instance
class TenderSurveyResourceContractorsOVendorsContractorDocumentDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PmsTenderSurveyDocument
        fields = '__all__'
    def update(self, instance, validated_data):
        instance.status = False
        instance.is_deleted = True
        instance.save()
        return instance
class TenderSurveyResourceContractorsOVendorsVendorModelMasterAddSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    owned_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)

    class Meta:
        model = PmsTenderSurveyResourceContractorsOVendorsVendorModelMaster
        fields = ("id", "name", "created_by", "owned_by", 'status')
class TenderSurveyResourceContractorsOVendorsVendorAddSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    owned_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)
    model_name = serializers.SerializerMethodField(required=False)
    def get_model_name(self,PmsTenderSurveyResourceContractorsOVendorsVendor):
        m = PmsTenderSurveyResourceContractorsOVendorsVendorModelMaster.objects.filter(pk=PmsTenderSurveyResourceContractorsOVendorsVendor.model.id).values('name')
        # print('s_loc_d', s_loc_d)
        for e_m in m:
            return e_m['name']
        pass
    class Meta:
        model = PmsTenderSurveyResourceContractorsOVendorsVendor
        fields = (
        "id", 'tender', "name", 'model','model_name','hire', 'khoraki', 'latitude', 'longitude', 'address', "created_by",
        "owned_by", 'status')
class TenderSurveyResourceContractorsOVendorsVendorEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PmsTenderSurveyResourceContractorsOVendorsVendor
        fields = ("id", "name", 'model', 'hire', 'khoraki', 'latitude', 'longitude', 'address', "updated_by")
class TenderSurveyResourceContractorsOVendorsVendorDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PmsTenderSurveyResourceContractorsOVendorsVendor
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.status = False
        instance.is_deleted = True
        instance.save()
        return instance
class TenderSurveyResourceContractorsOVendorsVendorDocumentAddSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    owned_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PmsTenderSurveyDocument
        fields = ("id", "tender", "module_id", "document_name", "document", "created_by", "owned_by")

    def create(self, validated_data):
        survey_document_data = PmsTenderSurveyDocument.objects.create(**validated_data,
                                                                      model_class="PmsTenderSurveyResourceContractorsOVendorsVendor")
        return survey_document_data
class TenderSurveyResourceContractorsOVendorsVendorDocumentEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PmsTenderSurveyDocument
        fields = ("id", "module_id", "document_name", "document", "updated_by")

    def update(self, instance, validated_data):
        instance.module_id = validated_data.get('module_id')
        instance.document_name = validated_data.get('document_name')
        instance.updated_by = validated_data.get('updated_by')
        existing_image = './media/' + str(instance.document)
        if validated_data.get('document'):
            if os.path.isfile(existing_image):
                os.remove(existing_image)
            instance.document = validated_data.get('document')
        instance.save()
        return instance
class TenderSurveyResourceContractorsOVendorsVendorDocumentDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PmsTenderSurveyDocument
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.status = False
        instance.is_deleted = True
        instance.save()
        return instance

#:::: TENDER SURVEY RESOURCE CONTACT DETAILS AND DESIGNATION :::::::#
class TenderSurveyResourceContactDesignationAddSerializer(serializers.ModelSerializer):
    status = serializers.BooleanField(default=True)
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model=PmsTenderSurveyResourceContactDesignation
        fields=('id','tender','name','status','created_by','owned_by')
class TenderSurveyResourceContactDetailsAddSerializer(serializers.ModelSerializer):
    status = serializers.BooleanField(default=True)
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PmsTenderSurveyResourceContactDetails
        fields = ('id', 'designation', 'field_label', 'field_value', 'status', 'created_by', 'owned_by')
class TenderSurveyResourceContactDetailsEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PmsTenderSurveyResourceContactDetails
        fields = ('id', 'designation', 'field_label', 'field_value',
                  'updated_by')
class TenderSurveyResourceContactDetailsDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PmsTenderSurveyResourceContactDetails
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.status = False
        instance.is_deleted = True
        instance.save()

        return instance

#::::::::::: TENDER INITIAL COSTING ::::::::::::::::::::#
class TenderInitialCostingUploadFileSerializer(serializers.ModelSerializer):
    field_label = serializers.CharField(required=False)
    field_value = serializers.CharField(required=False)
    class Meta:
        model=PmsTenderInitialCosting
        fields=('id','tender','document')
    def create(self, validated_data):
        try:
            #tender_initial_costing=PmsTenderInitialCosting.objects.create(**validated_data)
            import pandas as pd
            import xlrd
            df = pd.read_excel(validated_data.get('document'))
            print("Column headings:")
            print(df.columns)
            for j in df.columns:
                print(df[j])
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
                    print(df[j][i])

            response_data={
                'id':tender_initial_costing.id,
                'tender':tender_initial_costing.tender,
                'field_label':df.columns,
                'field_value':'',
                'document': tender_initial_costing.document,
            }
            return response_data
        except Exception as e:
            raise APIException({'request_status': 0, 'msg': e})
class TenderInitialCostingAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)
    #tender_initial_costing = serializers.CharField(required=False)
    #field_label = serializers.CharField(required=False)
    #field_value = serializers.CharField(required=False)
    #initial_costing_field_label = serializers.CharField(required=False)
    field_label_value = serializers.ListField(required=False)
    class Meta:
        model=PmsTenderInitialCosting
        fields=('id','tender','client','tender_notice_no_bid_id_no','name_of_work',
                'is_approved','received_estimate','quoted_rate','difference_in_budget',
                'document','status','created_by','owned_by','field_label_value')
    def create(self, validated_data):
        try:
            #print('validated_data',validated_data)
            field_label_value = validated_data.pop('field_label_value')
            tender_existing_data = PmsTenderInitialCosting.objects.get(tender=validated_data['tender'])
            print('tender_existing_data',tender_existing_data)
            if tender_existing_data:
                print('tender_existing_data11111', tender_existing_data.id)
                tender_existing_field_label = PmsTenderInitialCostingExcelFieldLabel.objects.filter(
                    tender_initial_costing=tender_existing_data.id).delete()

                tender_existing_field_value = PmsTenderInitialCostingExcelFieldValue.objects.filter(
                    tender_initial_costing=tender_existing_data.id).delete()



            else:
                print('tender_not_exist')
                tender_initial_costing=PmsTenderInitialCosting.objects.create(**validated_data)
                for each_field_label_value in field_label_value:
                    #print('each_field_label_value',each_field_label_value['field_label'])
                    tender_initial_costing_label = PmsTenderInitialCostingExcelFieldLabel.\
                        objects.create(
                        tender_initial_costing=PmsTenderInitialCosting.objects.get(pk=1),
                        field_label=each_field_label_value['field_label']
                    )
                    for field_value in each_field_label_value['field_value']:
                        tender_initial_costing_field = PmsTenderInitialCostingExcelFieldValue. \
                            objects.create(
                            tender_initial_costing=PmsTenderInitialCosting.objects.get(pk=1),
                            initial_costing_field_label=tender_initial_costing_label,
                            field_value=field_value

                        )
                    #print(df[j][i])

            response_data={
                'id':tender_initial_costing.id,
                'tender':tender_initial_costing.tender,
                'client': tender_initial_costing.client,
                'tender_notice_no_bid_id_no':tender_initial_costing.tender_notice_no_bid_id_no,
                'name_of_work':tender_initial_costing.name_of_work,
                'is_approved':tender_initial_costing.is_approved,
                'received_estimate': tender_initial_costing.received_estimate,
                'quoted_rate': tender_initial_costing.quoted_rate,
                'difference_in_budget': tender_initial_costing.difference_in_budget,
                'document': tender_initial_costing.document,
                'status':tender_initial_costing.status,
                'created_by':tender_initial_costing.created_by,
                'owned_by':tender_initial_costing.owned_by,
                'field_label_value':field_label_value
            }
            return response_data
        except Exception as e:
            raise APIException({'request_status': 0, 'msg': e})

#:::::::::::::::::  MECHINE WORKING CATEGORY :::::::::::#
class MachineriesWorkingCategoryAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PmsMachineriesWorkingCategory
        fields = ('id', 'name', 'created_by', 'owned_by')
class MachineriesWorkingCategoryEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PmsMachineriesWorkingCategory
        fields = ('id', 'name', 'updated_by')
class MachineriesWorkingCategoryDeleteSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = PmsMachineriesWorkingCategory
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.is_deleted = True
        instance.updated_by = validated_data.get('updated_by')
        instance.save()
        return instance

#:::::::::::::::::  MECHINARY MASTER :::::::::::::::#
class MachineriesAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    rental_details=serializers.DictField(required=False)
    owner_details=serializers.DictField(required=False)
    owner_emi_details=serializers.DictField(required=False)
    contract_details =serializers.DictField(required=False)

    class Meta:
        model = PmsMachineries

        fields = (
        'id', 'equipment_name', 'equipment_category', 'equipment_type', 'owner_type',
        'equipment_make',
        'equipment_model_no', 'equipment_registration_no',
        'equipment_chassis_serial_no',
        'equipment_engine_serial_no', 'equipment_power', 'measurement_by',
        'measurement_quantity',
        'fuel_consumption', 'remarks', 'created_by', 'owned_by', 'rental_details',
        'owner_details',
        'owner_emi_details', 'contract_details')

    def create(self, validated_data):
        try:
            #print('validated_data',validated_data)
            owner = validated_data.pop('owner_details') if 'owner_details' in validated_data else ""
            if 'is_emi_available' in owner and owner["is_emi_available"]:
                owner_emi = owner['owner_emi_details']
            contract = validated_data.pop('contract_details') if 'contract_details' in validated_data else ""
            rent = validated_data.pop('rental_details') if 'rental_details' in validated_data else ""
            owner_type = validated_data.get('owner_type')
            owned_by = validated_data.get('owned_by')
            created_by = validated_data.get('created_by')

            #print('owner["is_emi_available"]',owner["is_emi_available"])
            with transaction.atomic():
                machinary = PmsMachineries.objects.create(**validated_data)
                response = {
                    'id': machinary.id,
                    'equipment_name': machinary.equipment_name,
                    'equipment_category': machinary.equipment_category,
                    'equipment_type': machinary.equipment_type,
                    'owner_type': machinary.owner_type,
                    'equipment_make': machinary.equipment_make,
                    'equipment_model_no': machinary.equipment_model_no,
                    'equipment_registration_no': machinary.equipment_registration_no,
                    'equipment_chassis_serial_no': machinary.equipment_chassis_serial_no,
                    'equipment_engine_serial_no': machinary.equipment_engine_serial_no,
                    'equipment_power': machinary.equipment_power,
                    'measurement_by': machinary.measurement_by,
                    'measurement_quantity': machinary.measurement_quantity,
                    'fuel_consumption': machinary.fuel_consumption,
                    'remarks': machinary.remarks
                    }

                if owner_type == 1:
                    machinary_rental_details = PmsMachinaryRentedDetails.objects.create(
                                                                        equipment=machinary,
                                                                            vendor_id=int(rent['vendor']),
                                                                        rent_amount=rent['rent_amount'],
                                                                        type_of_rent_id=int(rent['type_of_rent']),
                                                                        owned_by = owned_by,
                                                                        created_by=created_by
                                                                        )
                    print('machinary_rental_details',machinary_rental_details)
                    rental_details_dict = {}
                    rental_details_dict["id"]=machinary_rental_details.id
                    rental_details_dict["equipment"]=machinary_rental_details.equipment.id
                    rental_details_dict["vendor"]=machinary_rental_details.vendor.id
                    rental_details_dict["type_of_rent"]=machinary_rental_details.type_of_rent.id
                    rental_details_dict["rent_amount"]=machinary_rental_details.rent_amount
                    response["rental_details"] = rental_details_dict
                elif owner_type == 2:
                    machinary_owner_details=PmsMachinaryOwnerDetails.objects.create(
                                                                    equipment=machinary,
                                                                    purchase_date=owner['purchase_date'],
                                                                    price = owner['price'],
                                                                    is_emi_available=owner["is_emi_available"],
                                                                    owned_by=owned_by,
                                                                    created_by=created_by
                                                                    )
                    owner_details_dict = {}
                    owner_details_dict["id"] = machinary_owner_details.id
                    owner_details_dict["equipment"] = machinary_owner_details.equipment.id
                    owner_details_dict["purchase_date"] = machinary_owner_details.purchase_date
                    owner_details_dict["price"] = machinary_owner_details.price
                    owner_details_dict["is_emi_available"] = machinary_owner_details.is_emi_available

                    if 'is_emi_available' in owner and owner["is_emi_available"]:
                        machinary_owner_emi_details=PmsMachinaryOwnerEmiDetails.objects.create(
                                                equipment=machinary,
                                                equipment_owner_details=machinary_owner_details,
                                                amount=owner_emi['amount'],
                                                start_date=owner_emi['start_date'],
                                                no_of_total_installment=owner_emi['no_of_total_installment'],

                                                owned_by=owned_by,
                                                created_by=created_by
                                                )
                        owner_emi_details = {}
                        owner_emi_details["id"] = machinary_owner_emi_details.id
                        owner_emi_details["equipment"] = machinary_owner_emi_details.equipment.id
                        owner_emi_details["equipment_owner_details"] = machinary_owner_emi_details.equipment_owner_details.id
                        owner_emi_details["amount"] = machinary_owner_emi_details.amount
                        owner_emi_details["start_date"] = machinary_owner_emi_details.start_date
                        owner_emi_details["no_of_total_installment"] = machinary_owner_emi_details.no_of_total_installment
                        #owner_emi_details["no_of_remain_installment"] = machinary_owner_emi_details.no_of_remain_installment
                        if owner_emi_details:
                            owner_details_dict["owner_emi_details"] = owner_emi_details
                    response["owner_details"] = owner_details_dict
                elif owner_type == 3:
                    print("contract['contractor_id']: ", contract['contractor'])
                    machinary_contract_details = PmsMachinaryContractDetails.objects.create(
                                                                equipment=machinary,
                                                                contractor_id=contract['contractor'],
                                                                owned_by=owned_by,
                                                                created_by=created_by
                                                            )
                    # print('query: ', machinary_contract_details.query)
                    contract_details = {}
                    contract_details["id"] = machinary_contract_details.id
                    contract_details["equipment"] = machinary_contract_details.equipment.id
                    contract_details["contractor"] = machinary_contract_details.contractor_id

                    response["contract_details"] = contract_details
                else:
                    pass
            return response
        except Exception as e:
            raise e
class MachineriesEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    equipment_category_details = serializers.DictField(required=False)
    document_details = serializers.ListField(required=False)
    rental_details = serializers.DictField(required=False)
    owner_details = serializers.DictField(required=False)
    owner_emi_details = serializers.DictField(required=False)
    contract_details = serializers.DictField(required=False)
    previous_owner_type = serializers.IntegerField(required=False)
    prev_emi_av = serializers.CharField(required=False)
    class Meta:
        model=PmsMachineries
        fields=('id', 'equipment_name', 'equipment_category', 'equipment_type', 'owner_type', 'equipment_make',
                'equipment_model_no', 'equipment_registration_no', 'equipment_chassis_serial_no',
                'equipment_engine_serial_no', 'equipment_power', 'measurement_by', 'measurement_quantity',
                'fuel_consumption', 'remarks', 'updated_by',
                'contract_details','owner_details','rental_details','owner_emi_details',
                'equipment_category_details','document_details','previous_owner_type','prev_emi_av')

    def update(self, instance, validated_data):
        owner = validated_data.pop('owner_details') if 'owner_details' in validated_data else ""
        if 'is_emi_available' in owner and owner["is_emi_available"]:
            owner_emi = owner['owner_emi_details']
            is_emi_available = True
        else:
            is_emi_available = False

        contract = validated_data.pop('contract_details') if 'contract_details' in validated_data else ""
        rent = validated_data.pop('rental_details') if 'rental_details' in validated_data else ""
        owner_type = validated_data.get('owner_type')
        previous_owner_type = validated_data.pop('previous_owner_type')

        instance.equipment_name = validated_data.get("equipment_name",instance.equipment_name)
        instance.equipment_category = validated_data.get("equipment_category",instance.equipment_category)
        instance.equipment_type = validated_data.get("equipment_type",instance.equipment_type)
        instance.owner_type = validated_data.get("owner_type",instance.owner_type)
        instance.equipment_make = validated_data.get("equipment_make",instance.equipment_make)
        instance.equipment_model_no = validated_data.get("equipment_model_no",instance.equipment_model_no)
        instance.equipment_registration_no = validated_data.get("equipment_registration_no", instance.equipment_registration_no)
        instance.equipment_chassis_serial_no = validated_data.get("equipment_chassis_serial_no", instance.equipment_chassis_serial_no)
        instance.equipment_engine_serial_no = validated_data.get("equipment_engine_serial_no", instance.equipment_engine_serial_no)
        instance.equipment_power = validated_data.get("equipment_power", instance.equipment_power)
        instance.measurement_by = validated_data.get("measurement_by", instance.measurement_by)
        instance.measurement_quantity = validated_data.get("measurement_quantity", instance.measurement_quantity)
        instance.fuel_consumption = validated_data.get("fuel_consumption", instance.fuel_consumption)
        instance.remarks = validated_data.get("remarks", instance.remarks)
        instance.updated_by = validated_data.get("updated_by", instance.updated_by)
        instance.save()
        response = {
            'id': instance.id,
            'equipment_name': instance.equipment_name,
            'equipment_category': instance.equipment_category,
            'equipment_type': instance.equipment_type,
            'owner_type': instance.owner_type,
            'equipment_make': instance.equipment_make,
            'equipment_model_no': instance.equipment_model_no,
            'equipment_registration_no': instance.equipment_registration_no,
            'equipment_chassis_serial_no': instance.equipment_chassis_serial_no,
            'equipment_engine_serial_no': instance.equipment_engine_serial_no,
            'equipment_power': instance.equipment_power,
            'measurement_by': instance.measurement_by,
            'measurement_quantity': instance.measurement_quantity,
            'fuel_consumption': instance.fuel_consumption,
            'remarks': instance.remarks
        }

        if previous_owner_type == 1:
            PmsMachinaryRentedDetails.objects.filter(equipment=instance).delete()
        elif previous_owner_type == 2:
            PmsMachinaryOwnerDetails.objects.filter(equipment=instance).delete()
        else:
            PmsMachinaryContractDetails.objects.filter(equipment=instance).delete()

        if owner_type == 1:
            machinary_rental_details = PmsMachinaryRentedDetails.objects.create(
                equipment=instance,
                vendor_id=int(rent['vendor']),
                rent_amount=rent['rent_amount'],
                type_of_rent_id=int(rent['type_of_rent']),
                owned_by=instance.updated_by,
                created_by=instance.updated_by
            )
            print('machinary_rental_details', machinary_rental_details)
            rental_details_dict = {}
            rental_details_dict["id"] = machinary_rental_details.id
            rental_details_dict["equipment"] = machinary_rental_details.equipment.id
            rental_details_dict["vendor"] = machinary_rental_details.vendor.id
            rental_details_dict["type_of_rent"] = machinary_rental_details.type_of_rent.id
            rental_details_dict["rent_amount"] = machinary_rental_details.rent_amount
            response["rental_details"] = rental_details_dict
        elif owner_type == 2:
            machinary_owner_details = PmsMachinaryOwnerDetails.objects.create(
                equipment=instance,
                purchase_date=owner['purchase_date'],
                price=owner['price'],
                is_emi_available=is_emi_available,
                owned_by=instance.updated_by,
                created_by=instance.updated_by
            )
            owner_details_dict = {}
            owner_details_dict["id"] = machinary_owner_details.id
            owner_details_dict["equipment"] = machinary_owner_details.equipment.id
            owner_details_dict["purchase_date"] = machinary_owner_details.purchase_date
            owner_details_dict["price"] = machinary_owner_details.price
            owner_details_dict["is_emi_available"] = machinary_owner_details.is_emi_available
            if owner["prev_emi_av"] == "yes":
                PmsMachinaryOwnerEmiDetails.objects.filter(equipment=instance).delete()
                if 'is_emi_available' in owner and owner["is_emi_available"]:
                    machinary_owner_emi_details = PmsMachinaryOwnerEmiDetails.objects.create(
                        equipment=instance,
                        equipment_owner_details=machinary_owner_details,
                        amount=owner_emi['amount'],
                        start_date=owner_emi['start_date'],
                        no_of_total_installment=owner_emi['no_of_total_installment'],
                        # no_of_remain_installment=owner_emi['purchase_date'],
                        owned_by=instance.updated_by,
                        created_by=instance.updated_by,
                    )
                    owner_emi_details = {}
                    owner_emi_details["id"] = machinary_owner_emi_details.id
                    owner_emi_details["equipment"] = machinary_owner_emi_details.equipment.id
                    owner_emi_details["equipment_owner_details"] = machinary_owner_emi_details.equipment_owner_details.id
                    owner_emi_details["amount"] = machinary_owner_emi_details.amount
                    owner_emi_details["start_date"] = machinary_owner_emi_details.start_date
                    owner_emi_details["no_of_total_installment"] = machinary_owner_emi_details.no_of_total_installment
                    # owner_emi_details["no_of_remain_installment"] = machinary_owner_emi_details.no_of_remain_installment
                    if owner_emi_details:
                        owner_details_dict["owner_emi_details"] = owner_emi_details
                response["owner_details"] = owner_details_dict
            else:
                if 'is_emi_available' in owner and owner["is_emi_available"]:
                    machinary_owner_emi_details = PmsMachinaryOwnerEmiDetails.objects.create(
                        equipment=instance,
                        equipment_owner_details=machinary_owner_details,
                        amount=owner_emi['amount'],
                        start_date=owner_emi['start_date'],
                        no_of_total_installment=owner_emi['no_of_total_installment'],
                        owned_by=instance.updated_by,
                        created_by=instance.updated_by
                    )
                    owner_emi_details = {}
                    owner_emi_details["id"] = machinary_owner_emi_details.id
                    owner_emi_details["equipment"] = machinary_owner_emi_details.equipment.id
                    owner_emi_details["equipment_owner_details"] = machinary_owner_emi_details.equipment_owner_details.id
                    owner_emi_details["amount"] = machinary_owner_emi_details.amount
                    owner_emi_details["start_date"] = machinary_owner_emi_details.start_date
                    owner_emi_details["no_of_total_installment"] = machinary_owner_emi_details.no_of_total_installment
                    # owner_emi_details["no_of_remain_installment"] = machinary_owner_emi_details.no_of_remain_installment
                    if owner_emi_details:
                        owner_details_dict["owner_emi_details"] = owner_emi_details
        else:
            machinary_contract_details = PmsMachinaryContractDetails.objects.create(
                equipment=instance,
                contractor_id=contract['contractor'],
                owned_by=instance.updated_by,
                created_by=instance.updated_by
            )
            # print('query: ', machinary_contract_details.query)
            contract_details = {}
            contract_details["id"] = machinary_contract_details.id
            contract_details["equipment"] = machinary_contract_details.equipment.id
            contract_details["contractor"] = machinary_contract_details.contractor_id
            response["contract_details"] = contract_details
        return response
class MachineriesListDetailsSerializer(serializers.ModelSerializer):
    equipment_category_details = serializers.SerializerMethodField()
    document_details = serializers.SerializerMethodField(required=False)
    def get_equipment_category_details(self, PmsMachineries):
        equipment = PmsMachineriesWorkingCategory.objects.filter(id=PmsMachineries.equipment_category.id)

        serializer = MachineriesWorkingCategoryAddSerializer(instance=equipment, many=True)
        return serializer.data[0]
    def get_document_details(self, PmsMachineries):
        document = PmsMachineriesDetailsDocument.objects.filter(equipment=PmsMachineries, is_deleted=False)
        request = self.context.get('request')
        response_list = []
        for each_document in document:
            file_url = request.build_absolute_uri(each_document.document.url)

            owned_by = str(each_document.owned_by) if each_document.owned_by else ''
            created_by = str(each_document.created_by) if each_document.created_by else ''
            each_data = {
                "id": int(each_document.id),
                "equipment": each_document.equipment.id,
                "document_name": each_document.document_name,
                "document": file_url,
                "created_by": created_by,
                "owned_by": owned_by
            }
            response_list.append(each_data)
        return response_list
    class Meta:
        model = PmsMachineries
        fields = ('id', 'equipment_name', 'equipment_category', 'equipment_category_details', 'equipment_type',
                  'owner_type', 'equipment_make',
                  'equipment_model_no', 'equipment_registration_no',
                  'equipment_chassis_serial_no',
                  'equipment_engine_serial_no', 'equipment_power', 'measurement_by',
                  'measurement_quantity', 'fuel_consumption', 'remarks',
                  'document_details')
class MachineriesDeleteSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = PmsMachineries
        fields = '__all__'
    def update(self, instance, validated_data):
        instance.is_deleted=True
        instance.updated_by = validated_data.get('updated_by')
        instance.save()
        return instance
class MachineriesDetailsDocumentAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PmsMachineriesDetailsDocument
        fields = ('id', 'equipment', 'document_name', 'document', 'created_by', 'owned_by')
class MachineriesDetailsDocumentEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PmsMachineriesDetailsDocument
        fields = ('id', 'equipment', 'document_name', 'updated_by')
class MachineriesDetailsDocumentDeleteSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PmsMachineriesDetailsDocument
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.is_deleted = True
        instance.updated_by = validated_data.get('updated_by')
        instance.save()
        return instance
class MachineriesDetailsDocumentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PmsMachineriesDetailsDocument
        fields = '__all__'

#:::::::::::::::::  PMS External Users ::::::::::::::::::::#
class ExternalUsersTypeAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    type_name = serializers.CharField(required=True)

    class Meta:
        model = PmsExternalUsersType
        fields = ('id', 'type_name', 'type_desc', 'created_by', 'owned_by')
class ExternalUsersTypeEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    type_name = serializers.CharField(read_only=True)

    class Meta:
        model = PmsExternalUsersType
        fields = ('id', 'type_name', 'type_desc', 'updated_by')
class ExternalUsersTypeDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PmsExternalUsersType
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.is_deleted = True
        instance.save()
        return instance

#:::::::::::::::::  PMS External Users Type ::::::::::::::::::::#
class ExternalUsersAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    name=serializers.CharField(required=True)
    # user_type=serializers.GenericForeignKey('content_type', 'olbject_id')
    # user_type=serializers.PrimaryKeyRelatedField(queryset=PmsExternalUsersType.objects.all())
    contact_no=serializers.CharField(required=True)
    email=serializers.CharField(required=True)
    address=serializers.CharField(required=True)
    document_details=serializers.SerializerMethodField()
    def get_document_details(self, PmsExternalUsers):
        document = PmsExternalUsersDocument.objects.filter(external_user=PmsExternalUsers.id,is_deleted=False)
        request = self.context.get('request')
        response_list = []
        for each_document in document:
            file_url = request.build_absolute_uri(each_document.document.url)
            owned_by = str(each_document.owned_by) if each_document.owned_by else ''
            created_by = str(each_document.created_by) if each_document.created_by else ''
            each_data = {
                "id": int(each_document.id),
                "external_user": each_document.external_user.id,
                "document_name": each_document.document_name,
                "document": file_url,
                "created_by": created_by,
                "owned_by": owned_by
            }
            response_list.append(each_data)
        return response_list
    class Meta:
        model = PmsExternalUsers
        fields = ('id', 'name', 'user_type','organisation_name', 'contact_no', 'email', 'address',
                  'created_by', 'owned_by','document_details')
class ExternalUsersEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    name = serializers.CharField(required=True)
    # user_type = serializers.CharField(required=True)
    contact_no = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    address = serializers.CharField(required=True)
    document_details = serializers.SerializerMethodField()
    def get_document_details(self, PmsExternalUsers):
        document = PmsExternalUsersDocument.objects.filter(external_user=PmsExternalUsers.id,is_deleted=False)
        request = self.context.get('request')
        response_list = []
        for each_document in document:
            file_url = request.build_absolute_uri(each_document.document.url)
            owned_by = str(each_document.owned_by) if each_document.owned_by else ''
            created_by = str(each_document.created_by) if each_document.created_by else ''
            each_data = {
                "id": int(each_document.id),
                "external_user": each_document.external_user.id,
                "document_name": each_document.document_name,
                "document": file_url,
                "created_by": created_by,
                "owned_by": owned_by
            }
            response_list.append(each_data)
        return response_list
    class Meta:
        model = PmsExternalUsers
        fields = ('id', 'name', 'user_type', 'organisation_name', 'contact_no', 'email', 'address',
        'updated_by','document_details')
class ExternalUsersDeleteSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model=PmsExternalUsers
        fields='__all__'
    def update(self, instance, validated_data):
        instance.is_deleted = True
        instance.updated_by = validated_data.get('updated_by')
        instance.save()
        return instance
class ExternalUsersDocumentAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = PmsExternalUsersDocument
        fields = ('id', 'external_user', 'document_name', 'document', 'created_by', 'owned_by')
class ExternalUsersDocumentEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PmsExternalUsersDocument
        fields = ('id', 'external_user', 'document_name', 'updated_by')
class ExternalUsersDocumentDeleteSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = PmsExternalUsersDocument
        fields = '__all__'
    def update(self, instance, validated_data):
        instance.is_deleted=True
        instance.updated_by = validated_data.get('updated_by')
        instance.save()
        return instance
class ExternalUsersDocumentListSerializer(serializers.ModelSerializer):
    class Meta:
        model=PmsExternalUsersDocument
        fields='__all__'

#---------------------------------- Pms Machinary Rented Type Master----------#
class MachinaryRentedTypeMasterAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = PmsMachinaryRentedTypeMaster
        fields = ('id', 'name', 'created_by', 'owned_by')
class MachinaryRentedTypeMasterEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PmsMachinaryRentedTypeMaster
        fields = ('id', 'name', 'updated_by')
class MachinaryRentedTypeMasterDeleteSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = PmsMachinaryRentedTypeMaster
        fields = '__all__'
    def update(self, instance, validated_data):
        instance.is_deleted=True
        instance.updated_by = validated_data.get('updated_by')
        instance.save()
        return instance

#-------------------------PmsTenderTabDocuments-------------------------------#
class TenderTabDocumentAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)
    is_upload_document=serializers.BooleanField(default=False)
    reason_for_no_documentation=serializers.CharField(required=False)
    class Meta:
        model = PmsTenderTabDocuments
        fields = ("id", "is_upload_document", "tender", "tender_eligibility", "document_date_o_s", "document_name","tab_document","reason_for_no_documentation", "created_by", "owned_by", 'status')
class TenderTabDocumentEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    is_upload_document = serializers.BooleanField(default=False)
    reason_for_no_documentation = serializers.CharField(required=False)
    class Meta:
        model=PmsTenderTabDocuments
        fields=('id','is_upload_document','tender_eligibility','document_date_o_s','document_name','tab_document','reason_for_no_documentation','updated_by')
    def update(self, instance, validated_data):
        instance.tender_eligibility = validated_data.get('tender_eligibility')
        instance.document_date_o_s = validated_data.get('document_date_o_s')
        instance.document_name = validated_data.get('document_name')
        instance.updated_by = validated_data.get('updated_by')
        existing_image = './media/' + str(instance.tab_document)
        print('existing_image',existing_image)
        if validated_data.get('tab_document'):
            if os.path.isfile(existing_image):
                os.remove(existing_image)
            instance.tab_document = validated_data.get('tab_document')
        instance.save()
        return instance
class TenderTabDocumentDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PmsTenderTabDocuments
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.status = False
        instance.is_deleted = True
        instance.save()
        return instance

#------------------------PmsTenderTabDocumentsPrice----------------------#
class TenderTabDocumentPriceAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)
    class Meta:
        model=PmsTenderTabDocumentsPrice
        fields=('id','tender','document_date_o_s','document_name','tab_document',"created_by", "owned_by", 'status')
class TenderTabDocumentPriceEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = PmsTenderTabDocumentsPrice
        fields = ( 'id','document_date_o_s', 'document_name', 'tab_document','updated_by')
    def update(self, instance, validated_data):
        instance.document_date_o_s = validated_data.get('document_date_o_s')
        instance.document_name = validated_data.get('document_name')
        instance.updated_by = validated_data.get('updated_by')
        existing_image = './media/' + str(instance.tab_document)
        print('existing_image', existing_image)
        if validated_data.get('tab_document'):
            if os.path.isfile(existing_image):
                os.remove(existing_image)
            instance.tab_document = validated_data.get('tab_document')
        instance.save()
        return instance
class TenderTabDocumentPriceDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PmsTenderTabDocumentsPrice
        fields = '__all__'
    def update(self, instance, validated_data):
        instance.status = False
        instance.is_deleted = True
        instance.save()
        return instance

#--------------------- Pms Site Type Project Site Management----------------#
class SiteTypeProjectSiteManagementAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = PmsSiteTypeProjectSiteManagement
        fields = ('id', 'name', 'created_by', 'owned_by')
class SiteTypeProjectSiteManagementEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PmsSiteTypeProjectSiteManagement
        fields = ('id', 'name', 'updated_by')
class SiteTypeProjectSiteManagementDeleteSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = PmsSiteTypeProjectSiteManagement
        fields = '__all__'
    def update(self, instance, validated_data):
        instance.is_deleted=True
        instance.updated_by = validated_data.get('updated_by')
        instance.save()
        return instance

#---------------------Pms Site Project Site Management----------------------#
class ProjectSiteManagementSiteAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    type_name = serializers.SerializerMethodField(required=False)
    def get_type_name(self,PmsSiteProjectSiteManagement):
        p_site = PmsSiteTypeProjectSiteManagement.objects.filter(pk=PmsSiteProjectSiteManagement.type.id).values('name')
        for e_p_site in p_site:
            return e_p_site['name']
    class Meta:
        model = PmsSiteProjectSiteManagement
        fields = ('id', 'name', 'address','latitude','longitude', 'type','type_name',
                  'description','company_name',
                  'gst_no', 'geo_fencing_area', 'created_by', 'owned_by')
class ProjectSiteManagementSiteEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PmsSiteProjectSiteManagement
        fields = ('id', 'name', 'address','latitude','longitude', 'type', 'description','company_name', 'gst_no', 'geo_fencing_area', 'updated_by')
class ProjectSiteManagementSiteDeleteSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = PmsSiteProjectSiteManagement
        fields = '__all__'
    def update(self, instance, validated_data):
        instance.is_deleted=True
        instance.updated_by = validated_data.get('updated_by')
        instance.save()
        return instance

#:::::::::::: PROJECTS ::::::::::::::::::::::::::::#
class ProjectsAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)

    class Meta:
        model = PmsProjects
        fields = ('id', 'tender', 'project_g_id', 'created_by', 'owned_by', 'status')
class ProjectsListSerializer(serializers.ModelSerializer):
    machinary_list = serializers.SerializerMethodField(required=False)
    tender_g_id = serializers.SerializerMethodField(required=False)
    site_location_name = serializers.SerializerMethodField(required=False)
    tender_bidder_type = serializers.SerializerMethodField(required=False)

    def get_machinary_list(self, PmsProjects):
        machinary_list = PmsProjectsMachinaryMapping.objects.filter(project=PmsProjects.id)
        m_list = list()
        for e_machinary in machinary_list:
            m_list.append(
                {'id': e_machinary.id,
                 'machinary': e_machinary.machinary.id,
                 'project': e_machinary.project.id,
                 'machinary_s_d_req': e_machinary.machinary_s_d_req,
                 'machinary_e_d_req': e_machinary.machinary_e_d_req
                 }
            )
        return m_list

    def get_tender_g_id(self, PmsProjects):
        tender_d = PmsTenders.objects.filter(pk=PmsProjects.tender.id).values('tender_g_id')
        # print('tender_d',tender_d)
        for e_tender in tender_d:
            return e_tender['tender_g_id']

    def get_site_location_name(self, PmsProjects):
        s_loc_d = PmsSiteProjectSiteManagement.objects.filter(pk=PmsProjects.site_location.id).values('name')
        # print('s_loc_d', s_loc_d)
        for e_s_loc in s_loc_d:
            return e_s_loc['name']

    def get_tender_bidder_type(self, PmsProjects):
        tender_b_t = PmsTenderBidderType.objects.filter(tender=PmsProjects.tender.id).values('bidder_type')
        for e_tender_b_t in tender_b_t:
            return e_tender_b_t['bidder_type'].replace("_", " ")

    class Meta:
        model = PmsProjects
        fields = ('id', 'tender', 'tender_g_id', 'project_g_id', 'name', 'site_location',
                  'site_location_name', 'tender_bidder_type', 'start_date',
                  'end_date', 'machinary_list', 'created_by',
                  'updated_by', 'owned_by', 'status')
class ProjectsEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    machinary_list = serializers.ListField(required=False)
    project_g_id = serializers.CharField(required=False)
    prev_machinary_list = serializers.CharField(required=False)
    employee_list = serializers.ListField(required=False)
    prev_employee_list = serializers.CharField(required=False)

    class Meta:
        model = PmsProjects
        fields = ('id', 'project_g_id', 'name', 'site_location', 'start_date',
                  'end_date', 'updated_by', 'machinary_list', "prev_machinary_list",
                  "prev_employee_list", "employee_list")

    def update(self, instance, validated_data):
        try:
            with transaction.atomic():

                #print('start_date_type',type(validated_data.get("start_date")))
                #print('start_date', validated_data.get("start_date"))
                response = dict()
                instance.name = validated_data.get("name")
                instance.site_location = validated_data.get("site_location")
                instance.start_date = validated_data.get("start_date")
                instance.end_date = validated_data.get("end_date")
                instance.save()
                prev_machinary_list = validated_data.get("prev_machinary_list")
                machinary_list = validated_data.get("machinary_list")
                prev_employee_list = validated_data.get("prev_employee_list")
                employee_list = validated_data.get("employee_list")
                m_list = list()
                e_list = list()
                #print('machinary_list',machinary_list)
                if prev_machinary_list == 'yes':
                    PmsProjectsMachinaryMapping.objects.filter(project=instance).delete()
                    for e_m in machinary_list:
                        machinary_s_d_req = e_m['machinary_s_d_req']
                        machinary_e_d_req = e_m['machinary_e_d_req']
                        machinary_s_d_req1 = datetime.datetime.strptime(machinary_s_d_req, "%Y-%m-%dT%H:%M:%S.%fZ")
                        machinary_e_d_req1 = datetime.datetime.strptime(machinary_e_d_req,"%Y-%m-%dT%H:%M:%S.%fZ")
                        MachinaryMapping = PmsProjectsMachinaryMapping.objects. \
                            create(
                            project=instance,
                            machinary_id=e_m['machinary'],
                            machinary_s_d_req=machinary_s_d_req1,
                            machinary_e_d_req=machinary_e_d_req1,
                            owned_by=instance.updated_by,
                            created_by=instance.updated_by
                        )
                        machinary_dict = {}
                        machinary_dict["id"] = MachinaryMapping.id
                        machinary_dict["project"] = MachinaryMapping.project.id
                        machinary_dict["machinary"] = MachinaryMapping.machinary.id
                        machinary_dict["machinary_s_d_req"] = MachinaryMapping.machinary_s_d_req
                        machinary_dict["machinary_e_d_req"] = MachinaryMapping.machinary_e_d_req
                        m_list.append(machinary_dict)
                else:
                    for e_m in machinary_list:
                        machinary_s_d_req = e_m['machinary_s_d_req']
                        machinary_e_d_req = e_m['machinary_e_d_req']
                        machinary_s_d_req1 = datetime.datetime.strptime(machinary_s_d_req, "%Y-%m-%dT%H:%M:%S.%fZ")
                        machinary_e_d_req1 = datetime.datetime.strptime(machinary_e_d_req, "%Y-%m-%dT%H:%M:%S.%fZ")
                        MachinaryMapping = PmsProjectsMachinaryMapping.objects. \
                            create(
                            project=instance,
                            machinary_id=e_m['machinary'],
                            machinary_s_d_req=machinary_s_d_req1,
                            machinary_e_d_req=machinary_e_d_req1,
                            owned_by=instance.updated_by,
                            created_by=instance.updated_by
                        )
                        # print('machinary_rental_details', machinary_rental_details)
                        machinary_dict = {}
                        machinary_dict["id"] = MachinaryMapping.id
                        machinary_dict["project"] = MachinaryMapping.project.id
                        machinary_dict["machinary"] = MachinaryMapping.machinary.id
                        machinary_dict["machinary_s_d_req"] = MachinaryMapping.machinary_s_d_req
                        machinary_dict["machinary_e_d_req"] = MachinaryMapping.machinary_e_d_req
                        m_list.append(machinary_dict)

                if prev_employee_list == 'yes':
                    PmsProjectUserMapping.objects.filter(project=instance).delete()
                    for e_l in employee_list:
                        start_date = e_l['start_date']
                        expire_date = e_l['expire_date']
                        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%fZ")
                        expire_date = datetime.datetime.strptime(expire_date, "%Y-%m-%dT%H:%M:%S.%fZ")
                        UserMapping = PmsProjectUserMapping.objects. \
                            create(
                            project=instance,
                            user_id=e_l['user'],
                            start_date=start_date,
                            expire_date=expire_date,
                            owned_by=instance.updated_by,
                            created_by=instance.updated_by
                        )
                        employee_dict = {}
                        employee_dict["id"] = UserMapping.id
                        employee_dict["project"] = UserMapping.project.id
                        employee_dict["user"] = UserMapping.user.id
                        employee_dict["start_date"] = UserMapping.start_date
                        employee_dict["expire_date"] = UserMapping.expire_date
                        e_list.append(employee_dict)
                else:
                    for e_l in employee_list:
                        start_date = e_l['start_date']
                        expire_date = e_l['expire_date']
                        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%fZ")
                        expire_date = datetime.datetime.strptime(expire_date, "%Y-%m-%dT%H:%M:%S.%fZ")
                        UserMapping = PmsProjectUserMapping.objects. \
                            create(
                            project=instance,
                            user_id=e_l['user'],
                            start_date=start_date,
                            expire_date=expire_date,
                            owned_by=instance.updated_by,
                            created_by=instance.updated_by
                        )
                        # print('machinary_rental_details', machinary_rental_details)
                        employee_dict = {}
                        employee_dict["id"] = UserMapping.id
                        employee_dict["project"] = UserMapping.project.id
                        employee_dict["user"] = UserMapping.user.id
                        employee_dict["start_date"] = UserMapping.start_date
                        employee_dict["expire_date"] = UserMapping.expire_date
                        e_list.append(employee_dict)
                response["id"] = instance.id
                response['project_g_id'] = instance.project_g_id
                response['name'] = instance.name
                response['site_location'] = instance.site_location
                response['start_date'] = instance.start_date
                response['end_date'] = instance.end_date
                response["machinary_list"] = m_list
                response["employee_list"] = e_list
                return response

        except Exception as e:
            raise APIException({"msg": e, "request_status": 0})
class ProjectsDeleteSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PmsProjects
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.status = False
        instance.is_deleted = True
        instance.updated_by = validated_data.get('updated_by')
        instance.save()
        m_m_list = PmsProjectsMachinaryMapping.objects.filter(project=instance)
        # print('m_m_list',m_m_list)
        for e_m in m_m_list:
            e_m.is_deleted = True
            e_m.updated_by = validated_data.get('updated_by')
            e_m.save()
        return instance
class ProjectDetailsSerializer(serializers.ModelSerializer):
    site_location = ProjectSiteManagementSiteAddSerializer()

    class Meta:
        model = PmsProjects
        fields = ('id', 'name', 'tender', 'site_location', 'start_date', 'end_date', 'status')

#:::::::::::: ATTENDENCE ::::::::::::#
class PmsAttendanceAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    employee = serializers.CharField(default=serializers.CurrentUserDefault())
    type = serializers.IntegerField(required=True)
    user_project_id = serializers.IntegerField(required=True)
    date = serializers.DateField(required=True)
    login_time = serializers.TimeField(required=True)
    login_latitude = serializers.CharField(required=True)
    login_longitude = serializers.CharField(required=True)
    login_address = serializers.CharField(required=True)

    class Meta:
        model = PmsAttendance
        fields = (
        'id', 'type', 'employee', 'user_project_id', 'date', 'login_time', 'login_latitude', 'login_longitude',
        'login_address', 'created_by', 'owned_by',)

    def create(self, validated_data):
        try:
            attendance_data = PmsAttendance.objects.create(**validated_data)
            print('attendance_data: ', attendance_data.type)
            return attendance_data
        except Exception as e:
            raise APIException({"msg": e, "request_status": 0})
class AttendanceLogOutSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PmsAttendance
        fields = ('id', 'logout_time', 'logout_latitude', 'logout_longitude', 'logout_address', 'updated_by')

    def update(self, instance, validated_data):
        instance.logout_time = validated_data.get("logout_time", instance.logout_time)
        instance.logout_latitude = validated_data.get("logout_latitude", instance.logout_latitude)
        instance.logout_longitude = validated_data.get("logout_longitude", instance.logout_longitude)
        instance.updated_by = validated_data.get("updated_by")
        instance.save()
        print("instance.attandance: ", type(instance.id))
        # log_details = PmsAttandanceLog.objects.filter()
        self.add_deviations(instance.id, instance.logout_time, instance.updated_by)
        return instance

    def add_deviations(self, att_id, log_out_time, owned_by):
        from datetime import timedelta
        owned_by = owned_by
        att_id = att_id

        log_details = PmsAttandanceLog.objects.filter(attandance_id=att_id)
        flag = 0
        check_len = 0
        for log in log_details:
            check_len += 1
            checkout = log.is_checkout
            if checkout == True:
                if flag == 1:
                    # if not to_time:
                    if check_len == len(log_details):
                        to_time = log_out_time
                        self.calculate_deviation(att_id, from_time, to_time, owned_by)
                else:
                    flag = 1
                    from_time = log.time
            else:
                if flag == 1:
                    flag = 0
                    to_time = log.time
                    self.calculate_deviation(att_id, from_time, to_time, owned_by)

    def calculate_deviation(self, att_id, from_time, to_time, owned_by):
        data_dict = {}
        dev_time = (to_time - from_time)
        time_deviation = (datetime.datetime.min + dev_time).time().strftime('%H:%M:%S')
        data_dict["attandance_id"] = att_id
        data_dict["from_time"] = from_time.strftime('%Y-%m-%dT%H:%M:%S')
        data_dict["to_time"] = to_time.strftime('%Y-%m-%dT%H:%M:%S')
        data_dict["deviation_time"] = time_deviation
        data_dict["owned_by"] = owned_by
        if dev_time.seconds <= 3600 * 5 and dev_time.seconds >= 3600 * 2.5:
            data_dict["deviation_type"] = "HD"
        elif dev_time.seconds > 3600 * 5:
            data_dict["deviation_type"] = "FD"
        else:
            data_dict["deviation_type"] = "OD"

        if data_dict:
            PmsAttandanceDeviation.objects.create(**data_dict)
class AttendanceAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    employee = serializers.CharField(default=serializers.CurrentUserDefault())
    date = serializers.DateTimeField(required=True)
    login_time = serializers.TimeField(required=True)

    # employee_details=serializers.SerializerMethodField()
    # def get_employee_details(self, PmsAttendance):
    #     from users.models import TCoreUserDetail
    #     from users.serializers import UserModuleSerializer, UserSerializer
    #     user_details = TCoreUserDetail.objects.filter(cu_user=PmsAttendance.employee)  # Whatever your query may be
    #     serializer = UserModuleSerializer(instance=user_details, many=True)
    #     return serializer.data
    class Meta:
        model = PmsAttendance
        fields = (
        'id', 'type', 'employee', 'user_project', 'date', 'login_time', 'login_latitude', 'login_longitude',
        'login_address',
        'logout_time', 'logout_latitude', 'logout_longitude', 'logout_address', 'approved_status', 'justification',
        'created_by', 'owned_by',)
class AttendanceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PmsAttendance
        fields = ('id', 'type', 'employee', 'user_project', 'date', 'login_time',
                  'logout_time', 'approved_status', 'justification')
class AttendanceSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PmsAttendance
        fields = (
        'id', 'type', 'employee', 'date', 'login_time', 'login_latitude', 'login_longitude', 'login_address',
        'logout_time', 'logout_latitude', 'logout_longitude', 'logout_address', 'approved_status', 'justification',
        'updated_by')
class AttendanceApprovalListSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    employee_details = serializers.SerializerMethodField()

    def get_employee_details(self, PmsAttendance):
        from users.models import TCoreUserDetail
        from users.serializers import UserModuleSerializer, UserSerializer
        user_details = TCoreUserDetail.objects.filter(cu_user=PmsAttendance.employee)  # Whatever your query may be
        serializer = UserModuleSerializer(instance=user_details, many=True)
        return serializer.data

    class Meta:
        model = PmsAttendance
        fields = (
        'id', 'type', 'employee', 'user_project', 'date', 'login_time', 'login_latitude', 'login_longitude',
        'login_address',
        'logout_time', 'logout_latitude', 'logout_longitude', 'logout_address', 'approved_status', 'justification',
        'created_by', 'owned_by', 'employee_details')
class AttandanceALLDetailsListSerializer(serializers.ModelSerializer):
    employee_details = serializers.SerializerMethodField()
    # log_details = serializers.SerializerMethodField()
    deviation_details = serializers.SerializerMethodField()
    user_project = ProjectDetailsSerializer()

    # def get_log_details(self, PmsAttendance):
    #     # print("PmsAttendance: ",PmsAttendance)
    #     attendance_log = PmsAttandanceLog.objects.filter(attandance_id=PmsAttendance.id)
    #     serializer = AttandanceLogSerializer(instance=attendance_log, many=True)
    #     # print("serializer.data: ",serializer.data)
    #     return serializer.data
    def get_employee_details(self, PmsAttendance):
        from users.models import TCoreUserDetail
        from users.serializers import UserModuleSerializer, UserSerializer
        user_details = TCoreUserDetail.objects.filter(cu_user=PmsAttendance.employee)  # Whatever your query may be
        serializer = UserModuleSerializer(instance=user_details, many=True)
        return serializer.data

    def get_deviation_details(self, PmsAttendance):
        # print("PmsAttendance: ",PmsAttendance)
        attendance_deviation = PmsAttandanceDeviation.objects.filter(attandance_id=PmsAttendance.id)
        serializer = AttandanceDeviationSerializer(instance=attendance_deviation, many=True)
        # print("serializer.data: ",serializer.data)
        return serializer.data

    class Meta:
        model = PmsAttendance
        fields = ('id', 'user_project', 'date', 'login_time',
                  'logout_time', 'approved_status', 'justification',
              'employee_details', 'deviation_details')

#:::::::::::: PmsAttandanceLog ::::::::::::#
class AttandanceLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PmsAttandanceLog
        fields = (
        'id', 'attandance', 'time', 'latitude', 'longitude', 'address', 'approved_status', 'justification',
        'remarks', 'is_checkout')
class AttandanceLogAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PmsAttandanceLog
        fields = (
        'id', 'attandance', 'time', 'latitude', 'longitude', 'address', 'approved_status', 'justification',
        'is_checkout', 'created_by', 'owned_by')

    def geofencing(self, cur_location, s_location, geo_fencing_area):
        try:

            if geo_fencing_area.endswith("km"):
                geo_fencing_area = re.findall('^\d+', geo_fencing_area)
                geo_fencing_area = int(geo_fencing_area[0]) * 1000

            else:
                geo_fencing_area = re.findall('^\d+', geo_fencing_area)
                geo_fencing_area = int(geo_fencing_area[0])

            distance = great_circle(cur_location, s_location).meters
            print("distance", distance)
            if distance > geo_fencing_area:
                return True
            else:
                return False
        except Exception as e:
            raise e

    def create(self, validated_data):
        try:
            # is_checkout=True
            attandance_id = validated_data.get('attandance')
            current_user = validated_data.get('created_by')
            latitude = validated_data.get('latitude')
            longitude = validated_data.get('longitude')
            cur_location = (latitude, longitude,)
            assign_project = PmsAttendance.objects.only('user_project_id').get(pk=attandance_id.id).user_project_id
            print("current_user: ", current_user)
            print("user_project_id: ", assign_project)
            # log_count = PmsAttandanceLog.objects.filter(attandance_id=attandance_id).count()
            if not assign_project:
                # print('log_count: ', log_count)
                if latitude and longitude:
                    import math
                    lat = float(latitude)
                    lon = float(longitude)
                    # R = 6378.1  # earth radius
                    R = 6371  # earth radius
                    distance = 30  # distance in km
                    lat1 = lat - math.degrees(distance / R)
                    lat2 = lat + math.degrees(distance / R)
                    long1 = lon - math.degrees(distance / R / math.cos(math.degrees(lat)))
                    long2 = lon + math.degrees(distance / R / math.cos(math.degrees(lat)))

                    site_details = PmsSiteProjectSiteManagement.objects.filter(
                        Q(latitude__gte=lat1, latitude__lte=lat2) | Q(longitude__gte=long1, longitude__lte=long2))
                    site_id_list = [i.id for i in site_details]
                    print("site_id_list: ", site_id_list)

                    project_user_mapping = PmsProjectUserMapping.objects.filter(user=current_user, status=True,
                                                                                project__site_location_id__in=site_id_list)[
                                           :1]
                    for project in project_user_mapping:
                        print('project_user_mapping: ', project.project_id)
                        site_lat = project.project.site_location.latitude
                        site_long = project.project.site_location.longitude
                        geo_fencing_area = project.project.site_location.geo_fencing_area
                        s_location = (site_lat, site_long,)
                        PmsAttendance.objects.filter(pk=attandance_id.id).update(user_project_id=project.project_id)
                        # is_checkout = self.geofencing(cur_location, s_location, geo_fencing_area)
            else:
                attandance_details = PmsAttendance.objects.filter(pk=attandance_id.id)
                for project in attandance_details:
                    print('attandance_project_id: ', project.user_project_id)
                    site_lat = project.user_project.site_location.latitude
                    site_long = project.user_project.site_location.longitude
                    geo_fencing_area = project.user_project.site_location.geo_fencing_area

                    s_location = (site_lat, site_long,)

            # print("cur_location: ", cur_location)
            # print("s_location: ", s_location)
            # print("geo_fencing_area: ", geo_fencing_area)
            is_checkout = self.geofencing(cur_location, s_location, geo_fencing_area)
            # print("is_checkout: ", is_checkout)
            attandance_log, created = PmsAttandanceLog.objects.get_or_create(**validated_data,
                                                                             is_checkout=is_checkout)
            print("created: ", created)
            return attandance_log
        except Exception as e:
            raise e
class AttandanceLogEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PmsAttandanceLog
        fields = ('id', 'justification', 'updated_by')

    def update(self, instance, validated_data):
        instance.justification = validated_data.get("justification", instance.justification)
        instance.updated_by = validated_data.get("updated_by")
        instance.save()
        return instance
class AttandanceLogApprovalEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PmsAttandanceLog
        fields = ('id', 'approved_status', 'remarks', 'updated_by')

    def put(self, instance, validated_data):
        instance.justification = validated_data.get("approved_status", instance.justification)
        instance.remarks = validated_data.get("remarks", instance.remarks)
        instance.updated_by = validated_data.get("updated_by")
        instance.save()
        return instance

#:::::::::::: Pms Attandance Deviation ::::::::::::#
class AttandanceDeviationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PmsAttandanceDeviation
        fields = "__all__"
class AttandanceDeviationJustificationEditSerializer(serializers.ModelSerializer):
    justified_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PmsAttandanceDeviation
        fields = ('id', 'justification', 'justified_by')

    def update(self, instance, validated_data):
        instance.justification = validated_data.get("justification", instance.justification)
        instance.justified_by = validated_data.get("justified_by")
        instance.save()
        return instance
class AttandanceDeviationApprovaEditSerializer(serializers.ModelSerializer):
    approved_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PmsAttandanceDeviation
        fields = ('id', 'approved_status', 'remarks', 'approved_by')

    def update(self, instance, validated_data):
        instance.approved_status = validated_data.get("approved_status", instance.approved_status)
        instance.remarks = validated_data.get("remarks", instance.remarks)
        instance.approved_by = validated_data.get("approved_by")
        instance.save()
        return instance

#:::::::::::: PmsAttandanceLeaves ::::::::::::#
class AdvanceLeavesAddSerializer(serializers.ModelSerializer):
    employee = serializers.CharField(default=serializers.CurrentUserDefault())
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PmsEmployeeLeaves
        fields = ('id', 'employee', 'leave_type', 'start_date', 'end_date', 'reason', 'created_by', 'owned_by')
class AdvanceLeaveEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PmsEmployeeLeaves
        fields = ('id', 'approved_status', 'updated_by')
class LeaveListByEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PmsEmployeeLeaves
        fields = ('id', 'employee', 'leave_type', 'start_date', 'end_date', 'reason',
                  'approved_status')

#:::::::::::::::::  MECHINARY REPORT :::::::::::::::#
class MachineriesReportAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    contractor_o_vendor_details = serializers.SerializerMethodField(required=False)
    machine_name = serializers.SerializerMethodField(required=False)
    def get_machine_name(self,PmsProjectsMachinaryReport):
        machin_d = PmsMachineries.objects.filter(pk=PmsProjectsMachinaryReport.machine.id).values('equipment_name')
        for e_machin_d in machin_d:
            return e_machin_d['equipment_name']
    def get_contractor_o_vendor_details(self,PmsProjectsMachinaryReport):
        machinary_d = PmsMachineries.objects.filter(pk=PmsProjectsMachinaryReport.machine.id)
        #print('machinary_d',machinary_d)
        response_d = dict()
        for e_mechine_details in machinary_d:
            #print('e_mechine_details',e_mechine_details.owner_type)
            if e_mechine_details.owner_type == 1:
                # print('xyz',gfsdsdf)
                machinary_rented_details_queryset = PmsMachinaryRentedDetails.objects.filter(
                    equipment=e_mechine_details.id,
                    is_deleted=False)
                # print('machinary_rented_details_queryset',machinary_rented_details_queryset)
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
                        pk=machinary_rent.vendor.id, is_deleted=False)
                    #print('m_rented_details_vendor', m_rented_details_vendor)
                    for e_m_rented_details_vendor in m_rented_details_vendor:
                        m_v_details = {'id': e_m_rented_details_vendor.id,
                                       'name': e_m_rented_details_vendor.name,
                                       'is_deleted': e_m_rented_details_vendor.is_deleted,
                                       }
                    response_d["rental_details"]['vendor_details'] = m_v_details
            elif e_mechine_details.owner_type == 2:
                owner_queryset = PmsMachinaryOwnerDetails.objects.filter(equipment=e_mechine_details.id,
                                                                         is_deleted=False)
                # print('owner_queryset',owner_queryset)
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
                        # print('emi_queryset',emi_queryset)
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
                            # print('owner_dict',owner_dict)
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
        return response_d
        pass
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.required:
            self.fields[field].required = True
        for field in self.Meta.allow_null:
            self.fields[field].allow_null = True
    class Meta:
        model = PmsProjectsMachinaryReport
        fields = (
        'id', 'machine','machine_name','date', 'opening_balance', 'cash_purchase',
        'diesel_transfer_from_other_site','total_diesel_available','total_diesel_consumed','diesel_balance',
        'diesel_consumption_by_equipment','other_consumption','miscellaneous_consumption',
        'opening_meter_reading', 'closing_meter_reading','running_km','running_hours', 'purpose',
        'last_pm_date','next_pm_schedule','difference_in_reading','hsd_average','standard_avg_of_hours',
        'created_by', 'owned_by','contractor_o_vendor_details')
        required = ('machine','date',)
        allow_null = ('last_pm_date','next_pm_schedule',)
class MachineriesReportEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.required:
            self.fields[field].required = True
        for field in self.Meta.allow_null:
            self.fields[field].allow_null = True
    class Meta:
        model = PmsProjectsMachinaryReport
        fields = ('id', 'machine', 'date', 'opening_balance', 'cash_purchase',
        'diesel_transfer_from_other_site','total_diesel_available','total_diesel_consumed','diesel_balance',
        'diesel_consumption_by_equipment','other_consumption','miscellaneous_consumption',
        'opening_meter_reading', 'closing_meter_reading','running_km','running_hours', 'purpose',
        'last_pm_date','next_pm_schedule','difference_in_reading','hsd_average',
        'standard_avg_of_hours','updated_by')
        required = ('machine','date',)
        allow_null = ('last_pm_date', 'next_pm_schedule',)