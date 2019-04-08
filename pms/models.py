from django.db import models
from django.contrib.auth.models import User
from dynamic_media import get_directory_path
from django_mysql.models import EnumField
from validators import validate_file_extension
from core.models import TCoreUnit
import datetime
import time
#:::::::::: LOG TABLE ::::::::#
class PmsLog(models.Model):
    module_id = models.BigIntegerField()
    module_table_name = models.TextField(blank=True, null=True)
    action_type = EnumField(choices=['add', 'edit', 'delete'])
    current_module_data = models.TextField(blank=True, null=True)
    updated_module_data = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_log'

#:::::::::: ADD NEW TENDER TABLE ::::::::#
class PmsTenders(models.Model):
    tender_g_id = models.CharField(max_length=50,unique=True)
    tender_final_date = models.DateTimeField(auto_now_add=False,blank=True, null=True)
    tender_opened_on = models.DateTimeField(auto_now_add=False,blank=True, null=True)
    tender_added_by = models.CharField(max_length=100, blank=True, null=True)
    tender_received_on = models.DateTimeField(auto_now_add=False,blank=True, null=True)
    tender_aasigned_to = models.CharField(max_length=100, blank=True, null=True)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_created_by',
                                   on_delete=models.CASCADE,blank=True,null=True)
    owned_by = models.ForeignKey(User, related_name='t_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='t_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_tenders'

#:::::::::: TENDER DOCUMENT TABLE ::::::::#
class PmsTenderDocuments(models.Model):
    tender = models.ForeignKey(PmsTenders,
                               related_name='t_d_tender_id',
                               on_delete=models.CASCADE,
                               blank=True,null=True)
    document_name = models.CharField(max_length=200,blank=True,null=True)
    tender_document = models.FileField(upload_to=get_directory_path,
                                        default=None,
                                        blank=True, null=True,
                                        validators=[validate_file_extension]
                                       )
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_d_created_by',
                                   on_delete=models.CASCADE,blank=True,null=True)
    owned_by = models.ForeignKey(User, related_name='t_d_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='t_d_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_tender_documents'

#:::::::::: TENDER  ELIGIBILITY  TABLE ::::::::#
class PmsTenderEligibility(models.Model):
    tender = models.ForeignKey(PmsTenders,
                                  related_name='t_e_tender_id',
                                  on_delete=models.CASCADE,
                                  blank=True,
                                  null=True
                                  )
    type = EnumField(choices=['technical', 'financial', 'special'])
    ineligibility_reason = models.TextField(blank=True, null=True)
    eligibility_status = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_e_created_by',
                                   on_delete=models.CASCADE,blank=True,null=True)
    owned_by = models.ForeignKey(User, related_name='t_e_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='t_e_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_tender_eligibility'
        unique_together = ('type', 'tender')

#:::::::::: TENDER  ELIGIBILITY FIELDS BY TYPE TABLE ::::::::#
class PmsTenderEligibilityFieldsByType(models.Model):
    tender = models.ForeignKey(PmsTenders,
                                  related_name='t_e_f_tender_id',
                                  on_delete=models.CASCADE,
                                  blank=True,
                                  null=True
                                  )
    tender_eligibility = models.ForeignKey(PmsTenderEligibility,
                                  related_name='eligibility_id',
                                  on_delete=models.CASCADE,
                                  blank=True,
                                  null=True
                                  )
    field_label = models.TextField(blank=True, null=True)
    field_value = models.TextField(blank=True, null=True)
    eligible = models.BooleanField(default=True)
    # document = models.FileField(upload_to=get_directory_path,
    #                             default=None,
    #                             blank=True, null=True,
    #                             validators=[validate_file_extension]
    #                             )
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_e_f_created_by',
                                   on_delete=models.CASCADE,blank=True,null=True)
    owned_by = models.ForeignKey(User, related_name='t_e_f_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='t_e_f_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_tender_eligibility_fields_by_type'

#:::::::::: TENDER VENDORS TABLE ::::::::#
class PmsTenderVendors(models.Model):
    tender = models.ForeignKey(PmsTenders,
                               related_name='t_v_tender_id',
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True
                               )
    name = models.CharField(max_length=80,blank=True,null=True)
    contact = models.CharField(max_length=30, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_v_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='t_v_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='t_v_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'pms_tender_vendors'

#:::::::::: TENDER  BIDDER TYPE TABLE ::::::::#
class PmsTenderBidderType(models.Model):
    type_of_partner = (
        (1, 'lead_partner'),
        (2, 'other_partner')
    )
    tender = models.ForeignKey(PmsTenders,
                                  related_name='t_b_t_tender_id',
                                  on_delete=models.CASCADE,
                                  blank=True,
                                  null=True
                                  )
    bidder_type = EnumField(choices=['joint_venture', 'individual'])
    type_of_partner = models.IntegerField(choices=type_of_partner,null=True,blank=True)
    responsibility = EnumField(choices=['technical', 'financial','technical_and_financial'],null=True,
                                                                    blank=True,)
    profit_sharing_ratio_actual_amount = models.FloatField(null=True, blank=True, default=None)
    profit_sharing_ratio_tender_specific_amount = models.FloatField(null=True,
                                                                    blank=True,
                                                                    default=None)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_b_t_created_by',
                                   on_delete=models.CASCADE,blank=True,null=True)
    owned_by = models.ForeignKey(User, related_name='t_b_t_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='t_b_t_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_tender_bidder_type'

#:::::::::: TENDER  BIDDER TYPE TABLE ::::::::#
class PmsTenderBidderTypeVendorMapping(models.Model):
    tender_bidder_type = models.ForeignKey(PmsTenderBidderType,on_delete=models.CASCADE,
                                  blank=True,null=True)
    tender_vendor = models.ForeignKey(PmsTenderVendors,on_delete=models.CASCADE,
                                  blank=True,null=True)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_b_t_v_m_created_by',
                                   on_delete=models.CASCADE,blank=True,null=True)
    owned_by = models.ForeignKey(User, related_name='t_b_t_v_m_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_tender_bidder_type_vendor_mapping'

#:::::::::: TENDER APPROVAL ::::::::#
class PmsTenderApproval(models.Model):
    tender = models.ForeignKey(PmsTenders,
                               related_name='t_a_tender_id',
                               on_delete=models.CASCADE,
                               blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    reject_reason = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_a_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='t_a_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='t_a_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'pms_tender_approval'

##################################################################################
########################### SURVEY TAB SECTION ###################################
##################################################################################

#:::::::::: TENDER SURVEY SITE PHOTOS ::::::::#
class PmsTenderSurveySitePhotos(models.Model):
    tender = models.ForeignKey(PmsTenders,
                                  related_name='t_s_s_p_tender_id',
                                  on_delete=models.CASCADE,
                                  blank=True,
                                  null=True
                                  )

    latitude = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.CharField(max_length=200, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    additional_notes = models.TextField(blank=True, null=True)
    document_name = models.CharField(max_length=100, blank=True, null=True)
    document = models.FileField(upload_to=get_directory_path,
                                       default=None,
                                       blank=True, null=True,
                                       validators=[validate_file_extension]
                                       )
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_s_s_p_created_by',
                                   on_delete=models.CASCADE,blank=True,null=True)
    owned_by = models.ForeignKey(User, related_name='t_s_s_p_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='t_s_s_p_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_tender_survey_site_photos'

#::: TENDER SURVEY COORDINATES SITE COORDINATE ::::#
class PmsTenderSurveyCoordinatesSiteCoordinate(models.Model):
    tender = models.ForeignKey(PmsTenders,
                                  related_name='t_s_c_s_c_tender_id',
                                  on_delete=models.CASCADE,
                                  blank=True,
                                  null=True
                                  )
    name = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.CharField(max_length=200, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_s_c_s_c_created_by',
                                   on_delete=models.CASCADE,blank=True,null=True)
    owned_by = models.ForeignKey(User, related_name='t_s_c_s_c_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='t_s_c_s_c_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_tender_survey_coordinates_site_coordinate'

#::: TENDER SURVEY MATERIALS ::::#
#[this table Common for resource->material,coordinates]
class PmsTenderSurveyMaterials(models.Model):
    tender = models.ForeignKey(PmsTenders,
                               related_name='t_s_m_tender_id',
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True
                               )
    name = models.CharField(max_length=200, blank=True, null=True)
    unit = models.ForeignKey(TCoreUnit,
                              on_delete=models.CASCADE,
                              blank=True,
                              null=True
                            )

    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_s_m_created_by',
                                   on_delete=models.CASCADE,blank=True,null=True)
    owned_by = models.ForeignKey(User, related_name='t_s_m_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='t_s_m_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_tender_survey_materials'

#::: TENDER SURVEY COORDINATES SUPPLIERS ::::#
class PmsTenderSurveyCoordinatesSuppliers(models.Model):
    Type_of_materials = (
        (1, 'raw_materials'),
        (2, 'crusher')
    )
    tender = models.ForeignKey(PmsTenders,
                                  related_name='t_s_c_s_tender_id',
                                  on_delete=models.CASCADE,
                                  blank=True,
                                  null=True
                                  )
    type = models.IntegerField(choices=Type_of_materials, null=True, blank=True)
    tender_survey_material = models.ForeignKey(PmsTenderSurveyMaterials,
                                  related_name='t_s_c_s_material_id',on_delete=models.CASCADE,
                                  blank=True,
                                  null=True
                                  )
    supplier_name = models.CharField(max_length=100, blank=True, null=True)
    contact = models.CharField(max_length=30, blank=True, null=True)
    latitude = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.CharField(max_length=200, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_s_c_s_created_by',
                                   on_delete=models.CASCADE,blank=True,null=True)
    owned_by = models.ForeignKey(User, related_name='t_s_c_s_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='t_s_c_s_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_tender_survey_coordinates_suppliers'
class PmsTenderSurveyCoordinatesSuppliersDocument(models.Model):
    coordinate_supplier = models.ForeignKey(PmsTenderSurveyCoordinatesSuppliers, related_name='t_s_c_s_doc',
                                            on_delete=models.CASCADE, blank=True, null=True)

    document_name = models.CharField(max_length=100, blank=True, null=True)
    document = models.FileField(upload_to=get_directory_path,
                                default=None,
                                blank=True, null=True,
                                validators=[validate_file_extension]
                                )
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_s_c_s_d_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='t_s_c_s_d_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='t_s_c_s_d_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'pms_tender_survey_coordinates_suppliers_document'

#::: TENDER SURVEY RESOURCE MATERIAL ::::#
class PmsTenderSurveyResourceMaterial(models.Model):
    tender = models.ForeignKey(PmsTenders,
                                  related_name='t_s_r_m_tender_id',
                                  on_delete=models.CASCADE,
                                  blank=True,
                                  null=True
                                  )
    tender_survey_material = models.ForeignKey(PmsTenderSurveyMaterials,
                                               related_name='t_s_r_m_material_id',
                                               on_delete=models.CASCADE,
                                               blank=True,
                                               null=True
                                               )
    supplier_name = models.CharField(max_length=100, blank=True, null=True)
    rate = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=3)
    latitude = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.CharField(max_length=200, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_s_r_m_created_by',
                                   on_delete=models.CASCADE,blank=True,null=True)
    owned_by = models.ForeignKey(User, related_name='t_s_r_m_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='t_s_r_m_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_tender_survey_resource_material'
class PmsTenderSurveyResourceMaterialDocument(models.Model):
    survey_resource_material = models.ForeignKey(PmsTenderSurveyResourceMaterial,
                                                 related_name='t_s_r_material_id',
                                                 on_delete=models.CASCADE,
                                                 blank=True,
                                                 null=True
                                                 )
    document_name = models.CharField(max_length=100, blank=True, null=True)
    document = models.FileField(upload_to=get_directory_path,
                                default=None,
                                blank=True, null=True,
                                validators=[validate_file_extension]
                                )

    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_s_r_m_d_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='t_s_r_m_d_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='t_s_r_m_d_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'pms_tender_survey_resource_material_document'

#::: TENDER SURVEY RESOURCE ESTABLISHMENT ::::#
class PmsTenderSurveyResourceEstablishment(models.Model):
    tender = models.ForeignKey(PmsTenders,
                                  related_name='t_s_r_e_tender_id',
                                  on_delete=models.CASCADE,
                                  blank=True,
                                  null=True
                                  )
    name = models.CharField(max_length=100, blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    latitude = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.CharField(max_length=200, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_s_r_e_created_by',
                                   on_delete=models.CASCADE,blank=True,null=True)
    owned_by = models.ForeignKey(User, related_name='t_s_r_e_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='t_s_r_e_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_tender_survey_resource_establishment'

#::: TENDER SURVEY DOCUMENT COMMON FOR THEREE TAB
# establishment,hydrological data,contractors/vendors ::::#
class PmsTenderSurveyDocument(models.Model):
    tender = models.ForeignKey(PmsTenders,
                               related_name='t_s_d_tender_id',
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True
                               )
    model_class = models.CharField(max_length=100, blank=True, null=True)
    module_id = models.IntegerField(blank=True, null=True)
    document_name = models.CharField(max_length=100,blank=True, null=True)
    document = models.FileField(upload_to=get_directory_path,
                                       default=None,
                                       blank=True, null=True,
                                       validators=[validate_file_extension]
                                       )
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_s_d_created_by',
                                   on_delete=models.CASCADE,blank=True,null=True)
    owned_by = models.ForeignKey(User, related_name='t_s_d_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='t_s_d_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_tender_survey_document'

#::: TENDER SURVEY RESOURCE HYDROLOGICAL ::::#
class PmsTenderSurveyResourceHydrological(models.Model):
    tender = models.ForeignKey(PmsTenders,
                                  related_name='t_s_r_h_tender_id',
                                  on_delete=models.CASCADE,
                                  blank=True,
                                  null=True
                                  )
    name = models.CharField(max_length=100,blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    latitude = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.CharField(max_length=200, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_s_r_h_created_by',
                                   on_delete=models.CASCADE,blank=True,null=True)
    owned_by = models.ForeignKey(User, related_name='t_s_r_h_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='t_s_r_h_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_tender_resource_hydrological'

#::: TENDER SURVEY RESOURCE CONTRACTORS OR VENDORS CONTRACTOR ::::#
class PmsTenderSurveyResourceContractorsOVendorsContractor(models.Model):
    tender = models.ForeignKey(PmsTenders,
                                  related_name='t_s_r_c_o_v_c_tender_id',
                                  on_delete=models.CASCADE,
                                  blank=True,
                                  null=True
                                  )
    name = models.CharField(max_length=100,blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    latitude = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.CharField(max_length=200, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_s_r_c_o_v_c_created_by',
                                   on_delete=models.CASCADE,blank=True,null=True)
    owned_by = models.ForeignKey(User, related_name='t_s_r_c_o_v_c_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='t_s_r_c_o_v_c_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_tender_resource_contractors_o_vendors_contractor'

#::: TENDER SURVEY RESOURCE CONTRACTORS OR VENDORS VENDOR MODEL MASTER ::::#
class PmsTenderSurveyResourceContractorsOVendorsVendorModelMaster(models.Model):
        name = models.CharField(max_length=100, blank=True, null=True)
        status = models.BooleanField(default=True)
        is_deleted = models.BooleanField(default=False)
        created_by = models.ForeignKey(User, related_name='t_s_r_c_o_v_v_v_m_created_by',
                                       on_delete=models.CASCADE, blank=True, null=True)
        owned_by = models.ForeignKey(User, related_name='t_s_r_c_o_v_v_v_m_owned_by',
                                     on_delete=models.CASCADE, blank=True, null=True)
        updated_by = models.ForeignKey(User, related_name='t_s_r_c_o_v_v_v_m_updated_by',
                                       on_delete=models.CASCADE, blank=True, null=True)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        def __str__(self):
            return str(self.id)

        class Meta:
            db_table = 'pms_tender_resource_contractors_o_vendors_vendor_model_master'

#::: TENDER SURVEY RESOURCE CONTRACTORS OR VENDORS VENDORS ::::#
class PmsTenderSurveyResourceContractorsOVendorsVendor(models.Model):
    tender = models.ForeignKey(PmsTenders,
                                  related_name='t_s_r_c_o_v_v_tender_id',
                                  on_delete=models.CASCADE,
                                  blank=True,
                                  null=True
                                  )
    name = models.CharField(max_length=100,blank=True, null=True)
    model = models.ForeignKey(PmsTenderSurveyResourceContractorsOVendorsVendorModelMaster,
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True
                               )
    hire = models.TextField(blank=True, null=True)
    khoraki = models.TextField(blank=True, null=True)
    latitude = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.CharField(max_length=200, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_s_r_c_o_v_v_created_by',
                                   on_delete=models.CASCADE,blank=True,null=True)
    owned_by = models.ForeignKey(User, related_name='t_s_r_c_o_v_v_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='t_s_r_c_o_v_v_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_tender_resource_contractors_o_vendors_vendor'

#::: TENDER SURVEY RESOURCE CONTACT DESIGNATION ::::#
class PmsTenderSurveyResourceContactDesignation(models.Model):
    tender = models.ForeignKey(PmsTenders,
                                  related_name='t_s_r_c_d_tender_id',
                                  on_delete=models.CASCADE,
                                  blank=True,
                                  null=True
                                  )
    name = models.CharField(max_length=100,blank=True, null=True)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_s_r_c_d_created_by',
                                   on_delete=models.CASCADE,blank=True,null=True)
    owned_by = models.ForeignKey(User, related_name='t_s_r_c_d_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='t_s_r_c_d_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_tender_resource_contact_designation'

#::: TENDER SURVEY RESOURCE CONTACT DETAILS ::::#
class PmsTenderSurveyResourceContactDetails(models.Model):
    designation = models.ForeignKey(PmsTenderSurveyResourceContactDesignation,
                                  related_name='t_s_r_c_d_designation_id',
                                  on_delete=models.CASCADE,
                                  blank=True,
                                  null=True
                                  )
    field_label = models.TextField(blank=True, null=True)
    field_value = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_s_r_c_de_created_by',
                                   on_delete=models.CASCADE,blank=True,null=True)
    owned_by = models.ForeignKey(User, related_name='t_s_r_c_de_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='t_s_r_c_de_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_tender_resource_contact_details'

#::: TENDER INITIAL COSTING ::::#
class PmsTenderInitialCosting(models.Model):
    tender = models.ForeignKey(PmsTenders,
                               related_name='t_i_c_tender_id',
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True
                               )
    client = models.CharField(max_length=100,blank=True, null=True)
    tender_notice_no_bid_id_no = models.CharField(max_length=100,
                                                  blank=True, null=True)
    name_of_work = models.TextField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    received_estimate = models.FloatField(blank=True, null=True)
    quoted_rate = models.FloatField(blank=True, null=True)
    difference_in_budget = models.FloatField(blank=True, null=True)
    document = models.FileField(upload_to=get_directory_path,default=None,
                                blank=True, null=True,
                                validators=[validate_file_extension]
                               )
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_i_c_created_by',
                                   on_delete=models.CASCADE,blank=True,null=True)
    owned_by = models.ForeignKey(User, related_name='t_i_c_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='t_i_c_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_tender_initial_costing'

#::: TENDER INITIAL COSTING EXCEL FIELD LABEL ::::#
class PmsTenderInitialCostingExcelFieldLabel(models.Model):
    tender_initial_costing = models.ForeignKey(PmsTenderInitialCosting,
                               related_name='t_i_c_e_f_l_costing_id',
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True
                               )
    field_label = models.CharField(max_length=100,blank=True, null=True)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_i_c_e_f_l_created_by',
                                   on_delete=models.CASCADE,blank=True,null=True)
    owned_by = models.ForeignKey(User, related_name='t_i_c_e_f_l_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='t_i_c_e_f_l_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_tender_initial_costing_excel_field_label'

#::: TENDER INITIAL COSTING EXCEL FIELD VALUE ::::#
class PmsTenderInitialCostingExcelFieldValue(models.Model):
    tender_initial_costing = models.ForeignKey(PmsTenderInitialCosting,
                               related_name='t_i_c_e_f_v_costing_id',
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True
                               )
    initial_costing_field_label = models.ForeignKey(PmsTenderInitialCostingExcelFieldLabel,
                               related_name='t_i_c_e_f_l_label_id',
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True
                               )
    field_value = models.CharField(max_length=100, blank=True, null=True)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_i_c_e_f_v_created_by',
                                   on_delete=models.CASCADE,blank=True,null=True)
    owned_by = models.ForeignKey(User, related_name='t_i_c_e_f_v_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='t_i_c_e_f_v_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_tender_initial_costing_excel_field_value'

#::: TENDER TAB DOCUMENTS ::::#
class PmsTenderTabDocuments(models.Model):
    tender= models.ForeignKey(PmsTenders,
                               related_name='t_t_d_tender_id',
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True
                               )
    tender_eligibility = models.ForeignKey(PmsTenderEligibility,
                               related_name='t_t_d_eligibility_id',
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True
                               )
    document_date_o_s = models.DateTimeField(blank=True,null=True)
    document_name = models.CharField(max_length=200, blank=True, null=True)
    tab_document = models.FileField(upload_to=get_directory_path,
                                       default=None,
                                       blank=True, null=True,
                                       validators=[validate_file_extension]
                                       )
    is_upload_document = models.BooleanField(default=False)
    reason_for_no_documentation=models.TextField(null=True,blank=True)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_t_d_created_by',
                                   on_delete=models.CASCADE,blank=True,null=True)
    owned_by = models.ForeignKey(User, related_name='t_t_d_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='t_t_d_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_tender_tab_documents'

#::: TENDER TAB DOCUMENTS PRICE ::::#
class PmsTenderTabDocumentsPrice(models.Model):
    tender= models.ForeignKey(PmsTenders,
                               related_name='t_t_d_p_tender_id',
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True
                               )
    document_date_o_s = models.DateTimeField(blank=True,null=True)
    document_name = models.CharField(max_length=200, blank=True, null=True)
    tab_document = models.FileField(upload_to=get_directory_path,
                                       default=None,
                                       blank=True, null=True,
                                       validators=[validate_file_extension]
                                       )
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_t_d_p_created_by',
                                   on_delete=models.CASCADE,blank=True,null=True)
    owned_by = models.ForeignKey(User, related_name='t_t_d_p_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='t_t_d_p_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_tender_tab_documents_price'

#::::::::::::::::Pms Site Type ProjectSiteManagement:::::::::::::::::::::::
class PmsSiteTypeProjectSiteManagement(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='site_type_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='site_type_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='site_type_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'pms_site_type_project_site_management'

#::::::::::::::::Pms Site ProjectSiteManagement:::::::::::::::::::::::
class PmsSiteProjectSiteManagement(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    latitude = models.DecimalField(max_digits=40,decimal_places=16, blank=True, null=True)
    longitude = models.DecimalField(max_digits=40,decimal_places=16, blank=True, null=True)
    type = models.ForeignKey(PmsSiteTypeProjectSiteManagement, related_name='project_site_management_type',
                             on_delete=models.CASCADE, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    gst_no = models.CharField(max_length=255, blank=True, null=True)
    geo_fencing_area = models.CharField(max_length=255, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='project_site_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='project_site_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='project_site_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'pms_site_project_site_management'

#::::::::::::::::  PROJECTS :::::::::::::::::::::::::::#
def unique_rand_project():
    while True:
        code = "P" + str(int(time.time()))
        if not PmsProjects.objects.filter(project_g_id=code).exists():
            return code
class PmsProjects(models.Model):
    name= models.CharField(max_length=200,blank=True,null=True)
    project_g_id = models.CharField(max_length=50, unique=True,
                                    default=unique_rand_project)
    tender=models.ForeignKey(PmsTenders,
                               related_name='p_tender_id',
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True
                               )
    site_location = models.ForeignKey(PmsSiteProjectSiteManagement,
                               related_name='p_s_management_id',
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True
                               )
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='p_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='p_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='p_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'pms_projects'

#:::  ATTENDENCE ::::#
class PmsAttendance(models.Model):
    Type_of_attandance= (
        (1, 'individual'),
        (2, ' labours under individual')
    )
    Type_of_approved = (
        (1, 'pending'),
        (2, 'approved'),
        (3, 'reject'),
        (4, 'regular'),
    )
    type = models.IntegerField(choices=Type_of_attandance, null=True, blank=True)
    employee=models.ForeignKey(User, related_name='attandance_employee_id',
                                   on_delete=models.CASCADE,blank=True,null=True)
    user_project = models.ForeignKey(PmsProjects, related_name='user_project',
                                   on_delete=models.CASCADE, blank=True, null=True)
    date= models.DateTimeField(auto_now_add=False,blank=True, null=True)
    login_time=models.DateTimeField(blank=True, null=True)
    login_latitude = models.CharField(max_length=200, blank=True, null=True)
    login_longitude= models.CharField(max_length=200, blank=True, null=True)
    login_address=models.TextField(blank=True, null=True)
    logout_time=models.DateTimeField(blank=True, null=True)
    logout_latitude = models.CharField(max_length=200, blank=True, null=True)
    logout_longitude = models.CharField(max_length=200, blank=True, null=True)
    logout_address = models.TextField(blank=True, null=True)
    approved_status = models.IntegerField(choices=Type_of_approved,
                                         default=4)
    justification=models.TextField(blank=True, null=True)
    # deviation_time = models.IntegerField(default=0)
    is_deleted= models.BooleanField(default=False)
    created_by =models.ForeignKey(User, related_name='attandance_created_by',
                                   on_delete=models.CASCADE,blank=True,null=True)
    owned_by = models.ForeignKey(User, related_name='attandance_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='attandance_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'pms_attandance'
class PmsAttandanceLog(models.Model):
  Type_of_approved = (
        (1, 'pending'),
        (2, 'approved'),
        (3, 'reject'),
        (4, 'regular'),
    )
  attandance=models.ForeignKey(PmsAttendance,related_name='a_l_attandance_id',
                                 on_delete=models.CASCADE,blank=True,null=True)
  time=models.DateTimeField(blank=True, null=True)
  latitude = models.CharField(max_length=200, blank=True, null=True)
  longitude = models.CharField(max_length=200, blank=True, null=True)
  address = models.TextField(blank=True, null=True)
  approved_status = models.IntegerField(choices=Type_of_approved, default=4)
  justification = models.TextField(blank=True, null=True)
  remarks=models.TextField(blank=True, null=True)
  is_checkout = models.BooleanField(default=False)
  is_deleted = models.BooleanField(default=False)
  created_by = models.ForeignKey(User, related_name='a_l_created_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
  owned_by = models.ForeignKey(User, related_name='a_l_owned_by',
                               on_delete=models.CASCADE, blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
      return str(self.id)

  class Meta:
      db_table = 'pms_attandance_log'
class PmsAttandanceDeviation(models.Model):
    Type_of_approved = (
        (1, 'pending'),
        (2, 'approved'),
        (3, 'reject'),
        (4, 'regular'),
    )
    Type_of_deviation = (('OD', 'official duty'),
                     ('HD', 'half day'),
                     ('FD', 'full day'))
    attandance = models.ForeignKey(PmsAttendance, related_name='a_d_attandance_id',
                                   on_delete=models.CASCADE, blank=True, null=True)
    from_time = models.DateTimeField(blank=True, null=True)
    to_time = models.DateTimeField(blank=True, null=True)
    deviation_time = models.CharField(max_length=10,blank=True, null=True)
    deviation_type = models.CharField(max_length=2,
                                  choices=Type_of_deviation,
                                  default="OD")
    justification = models.TextField(blank=True, null=True)
    approved_status = models.IntegerField(choices=Type_of_approved, default=4)
    remarks = models.TextField(blank=True, null=True)
    justified_by = models.ForeignKey(User, related_name='a_d_justified_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    justified_at = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(User, related_name='a_d_approved_by',
                                     on_delete=models.CASCADE, blank=True, null=True)
    approved_at = models.DateTimeField(auto_now_add=True)
    owned_by = models.ForeignKey(User, related_name='a_d_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'pms_attandance_deviation'
class PmsEmployeeLeaves(models.Model):
    Type_of_approved = (
        (1, 'pending'),
        (2, 'approved'),
        (3, 'reject'),
        (4, 'regular'),
    )

    Type_of_leave = (('EL', 'earned leave'),
                      ('CL', 'casual leave'),
                     ('AB', 'Absent'))
    employee = models.ForeignKey(User, related_name='leaves_employee_id',
                                 on_delete=models.CASCADE, blank=True, null=True)
    leave_type = models.CharField(max_length=2,
                  choices=Type_of_leave,
                  default="AB")

    start_date= models.DateTimeField(blank=True, null=True)
    end_date= models.DateTimeField(blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    approved_status = models.IntegerField(choices=Type_of_approved,
                                          default=1)

    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='leave_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='leave_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='leave_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'pms_employee_leaves'

# ::: PMS Machineries Working Category ::::::::::::::::::#
class PmsMachineriesWorkingCategory(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='machineries_working_category_created_by',
    on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='machineries_working_category_owned_by',
    on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='machineries_working_category_updated_by',
    on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'pms_machineries_working_category'

# ::: PMS External Users Type ::::::::::::::::::#
class PmsExternalUsersType(models.Model):
    type_name = models.CharField(max_length=200, blank=True, null=True)
    type_desc = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='external_users_type_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='external_users_type_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='external_users_type_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'pms_external_users_type'

# ::: PMS External Users ::::::::::::::::::#
class PmsExternalUsers(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    user_type = models.ForeignKey(PmsExternalUsersType, related_name='external_users_type',
                                  on_delete=models.CASCADE, blank=True, null=True)
    organisation_name = models.CharField(max_length=200, blank=True, null=True)
    contact_no = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField(max_length=70, blank=True, null=True, unique=True)
    address = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='external_users_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='external_users_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='external_users_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'pms_external_userso'
class PmsExternalUsersDocument(models.Model):
    external_user = models.ForeignKey(PmsExternalUsers, related_name='external_users_document',
                                      on_delete=models.CASCADE, blank=True, null=True)
    document_name = models.CharField(max_length=200, blank=True, null=True)
    document = models.FileField(upload_to=get_directory_path,
                                default=None,
                                blank=True, null=True,
                                validators=[validate_file_extension]
                                )
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='external_users_document_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='external_users_document_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='external_users_document_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'pms_external_users_document'

# ::: PMS Machineries ::::::::::::::::::#
class PmsMachineries(models.Model):
    Type_of_machineries = (
    (1, 'heavy_machinery'),
    (2, 'light_machinery')
    )

    Type_of_owner = (
    (1, 'rental'),
    (2, 'own'),
    (3, 'contract')
    )
    Type_of_measurement = (
    (1, 'distance'),
    (2, 'time')
    )

    equipment_name = models.CharField(max_length=200, blank=True, null=True)
    equipment_category = models.ForeignKey(PmsMachineriesWorkingCategory,related_name='equipment_working_category',
    on_delete=models.CASCADE,blank=True,null=True)
    equipment_type = models.IntegerField(choices=Type_of_machineries, null=True, blank=True)
    owner_type = models.IntegerField(choices=Type_of_owner, null=True, blank=True)
    equipment_make = models.CharField(max_length=200, blank=True, null=True)
    equipment_model_no = models.CharField(max_length=200, blank=True, null=True)
    equipment_chassis_serial_no = models.CharField(max_length=100, blank=True, null=True)
    equipment_engine_serial_no = models.CharField(max_length=100, blank=True, null=True)
    equipment_registration_no = models.CharField(max_length=200, blank=True, null=True)
    equipment_power = models.CharField(max_length=200, blank=True, null=True)
    measurement_by = models.IntegerField(choices=Type_of_measurement, null=True, blank=True)
    measurement_quantity = models.CharField(max_length=200, blank=True, null=True)
    fuel_consumption = models.CharField(max_length=100, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='machinery_created_by',
    on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='machinery_owned_by',
    on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='machinery_updated_by',
    on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'pms_machineries'
class PmsMachineriesDetailsDocument(models.Model):
    equipment = models.ForeignKey(PmsMachineries, related_name='equipment_machineries', on_delete=models.CASCADE,
                                  blank=True, null=True)
    document_name = models.CharField(max_length=200, blank=True, null=True)
    document = models.FileField(upload_to=get_directory_path,
                                default=None,
                                blank=True, null=True,
                                validators=[validate_file_extension]
                                )
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='machinery_document_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='machinery_document_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='machinery_document_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'pms_machineries_document'

#::::::::::Pms Machinary Rented Type Master:::::::::::#
class PmsMachinaryRentedTypeMaster(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='machinery_rented_type_master_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='machinery_rented_type_master_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='machinery_rented_type_master_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'pms_machinary_rented_type_master'

#::::::::::::Pms Machinary Rented Details::::::::::#
class PmsMachinaryRentedDetails(models.Model):
    equipment = models.ForeignKey(PmsMachineries, related_name='equipment_machineries_rented_details',
                                  on_delete=models.CASCADE, blank=True, null=True)
    vendor = models.ForeignKey(PmsExternalUsers, related_name='vendors_machineries_rented_details',
                                on_delete=models.CASCADE, blank=True, null=True)
    rent_amount = models.CharField(max_length=200, blank=True, null=True)
    type_of_rent = models.ForeignKey(PmsMachinaryRentedTypeMaster, related_name='machinary_rented_details',
                                     on_delete=models.CASCADE, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='machinery_rented_details_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='machinery_rented_details_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='machinery_rented_details_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'pms_machinary_rented_details'

#:::::::::::::Pms Machinary Owner Details:::::::::::::::::#
class PmsMachinaryOwnerDetails(models.Model):
    equipment = models.ForeignKey(PmsMachineries, related_name='machinary_owner_details',
                                  on_delete=models.CASCADE, blank=True, null=True)
    purchase_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    is_emi_available = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='machinery_owner_details_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='machinery_owner_details_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='machinery_owner_details_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'pms_machineries_owner_details'

#:::::::::::Pms Machinary Owner EMI Details:::::::::::::::::#
class PmsMachinaryOwnerEmiDetails(models.Model):
    equipment = models.ForeignKey(PmsMachineries, related_name='machinary_owner_emi_details',
                                  on_delete=models.CASCADE, blank=True, null=True)

    equipment_owner_details = models.ForeignKey(PmsMachinaryOwnerDetails,
                                                related_name='machinary_owner_emi_details',
                                                on_delete=models.CASCADE, blank=True, null=True)

    amount = models.FloatField(blank=True, null=True)
    start_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    no_of_total_installment = models.IntegerField(null=True, blank=True)
    #no_of_remain_installment = models.IntegerField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='machinery_owner_emi_details_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='machinery_owner_emi_details_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='machinery_owner_emi_details_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'pms_machineries_owner_emi_details'

#:::::::::Pms Machinary Contract Details:::::::::::::::::#
class PmsMachinaryContractDetails(models.Model):
    equipment = models.ForeignKey(PmsMachineries, related_name='machinary_contract_details',
                                  on_delete=models.CASCADE, blank=True, null=True)
    contractor = models.ForeignKey(PmsExternalUsers, related_name='machinary_contract_details_contractor',
                                   on_delete=models.CASCADE, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='machinery_contract_details_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='machinery_contract_details_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='machinery_contract_details_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'pms_machineries_contract_details'

#:::::::::::::::: PROJECTS MACHINARY MAPPING :::::::::::#
class PmsProjectsMachinaryMapping(models.Model):
    project = models.ForeignKey(PmsProjects,related_name='m_p_id',
                                on_delete=models.CASCADE,blank=True,null=True)
    machinary = models.ForeignKey(PmsMachineries,
                               related_name='m_machinary_id',
                               on_delete=models.CASCADE,blank=True,null=True
                               )
    machinary_s_d_req = models.DateTimeField(blank=True, null=True)
    machinary_e_d_req = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='m_m_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='m_m_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='m_m_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'pms_projects_machinary_mapping'

#:::::::::::::::: PROJECTS USER MAPPING :::::::::::#
class PmsProjectUserMapping(models.Model):
    project = models.ForeignKey(PmsProjects, related_name='project_user',
                                on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, related_name='project_user_mapping_user',
                             on_delete=models.CASCADE, blank=True, null=True)
    start_date = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    expire_date = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='p_u_m_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='p_u_m_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='p_u_m_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'pms_project_user_mapping'

#:::::::::::::::: PROJECTS MACHINARY REPORTS :::::::::::#
class PmsProjectsMachinaryReport(models.Model):
    machine = models.ForeignKey(PmsMachineries,related_name='m_r_machinary_id',
                               on_delete=models.CASCADE,blank=True,null=True)
    date = models.DateTimeField(blank=True, null=True)
    opening_balance = models.DecimalField(blank=True, null=True, max_digits=10,decimal_places=5)
    cash_purchase = models.DecimalField(blank=True, null=True,max_digits=10,decimal_places=5)
    diesel_transfer_from_other_site = models.DecimalField(blank=True, null=True,max_digits=10,decimal_places=5)
    total_diesel_available = models.DecimalField(blank=True, null=True, max_digits=10,decimal_places=5)
    total_diesel_consumed = models.DecimalField(blank=True, null=True, max_digits=10,decimal_places=5)
    diesel_balance = models.DecimalField(blank=True, null=True, max_digits=10,decimal_places=5)
    diesel_consumption_by_equipment = models.DecimalField(blank=True, null=True,max_digits=10,decimal_places=5)
    other_consumption = models.DecimalField(blank=True, null=True,max_digits=10,decimal_places=5)
    miscellaneous_consumption = models.DecimalField(blank=True, null=True,max_digits=10,decimal_places=5)
    opening_meter_reading = models.DecimalField(blank=True, null=True,max_digits=10,decimal_places=5)
    closing_meter_reading = models.DecimalField(blank=True, null=True,max_digits=10,decimal_places=5)
    running_km = models.DecimalField(blank=True, null=True,max_digits=10,decimal_places=5)
    running_hours = models.DecimalField(blank=True, null=True,max_digits=10,decimal_places=5)
    purpose = models.TextField(blank=True,null=True)
    last_pm_date = models.DateTimeField(blank=True, null=True)
    next_pm_schedule = models.DateTimeField(blank=True, null=True)
    difference_in_reading = models.DecimalField(blank=True, null=True,max_digits=10,decimal_places=5)
    hsd_average = models.DecimalField(blank=True, null=True,max_digits=10,decimal_places=5)
    standard_avg_of_hours = models.DecimalField(blank=True, null=True,max_digits=10,decimal_places=5)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='m_m_r_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='m_m_r_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='m_m_r_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_machinary_report'






