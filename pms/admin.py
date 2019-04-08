from django.contrib import admin
from pms.models import *

# Register your models here.
@admin.register(PmsLog)
class PmsLog(admin.ModelAdmin):
    list_display = [field.name for field in PmsLog._meta.fields]

@admin.register(PmsTenders)
class PmsTenders(admin.ModelAdmin):
    list_display = [field.name for field in PmsTenders._meta.fields]


@admin.register(PmsTenderDocuments)
class PmsTenderDocuments(admin.ModelAdmin):
    list_display = [field.name for field in PmsTenderDocuments._meta.fields]

@admin.register(PmsTenderEligibility)
class PmsTenderEligibility(admin.ModelAdmin):
    list_display = [field.name for field in PmsTenderEligibility._meta.fields]



@admin.register(PmsTenderEligibilityFieldsByType)
class PmsTenderEligibilityFieldsByType(admin.ModelAdmin):
    list_display = [field.name for field in PmsTenderEligibilityFieldsByType._meta.fields]


@admin.register(PmsTenderVendors)
class PmsTenderVendors(admin.ModelAdmin):
    list_display = [field.name for field in PmsTenderVendors._meta.fields]


@admin.register(PmsTenderBidderType)
class PmsTenderBidderType(admin.ModelAdmin):
    list_display = [field.name for field in PmsTenderBidderType._meta.fields]


@admin.register(PmsTenderBidderTypeVendorMapping)
class PmsTenderBidderTypeVendorMapping(admin.ModelAdmin):
    list_display = [field.name for field in PmsTenderBidderTypeVendorMapping._meta.fields]

@admin.register(PmsTenderSurveySitePhotos)
class PmsTenderSurveySitePhotos(admin.ModelAdmin):
    list_display = [field.name for field in PmsTenderSurveySitePhotos._meta.fields]


@admin.register(PmsTenderSurveyCoordinatesSiteCoordinate)
class PmsTenderSurveyCoordinatesSiteCoordinate(admin.ModelAdmin):
    list_display = [field.name for field in PmsTenderSurveyCoordinatesSiteCoordinate._meta.fields]

@admin.register(PmsTenderSurveyMaterials)
class PmsTenderSurveyMaterials(admin.ModelAdmin):
    list_display = [field.name for field in PmsTenderSurveyMaterials._meta.fields]


@admin.register(PmsTenderSurveyCoordinatesSuppliers)
class PmsTenderSurveyCoordinatesSuppliers(admin.ModelAdmin):
    list_display = [field.name for field in PmsTenderSurveyCoordinatesSuppliers._meta.fields]

@admin.register(PmsTenderSurveyCoordinatesSuppliersDocument)
class PmsTenderSurveyCoordinatesSuppliersDocument(admin.ModelAdmin):
    list_display = [field.name for field in PmsTenderSurveyCoordinatesSuppliersDocument._meta.fields]

@admin.register(PmsTenderSurveyResourceMaterial)
class PmsTenderSurveyResourceMaterial(admin.ModelAdmin):
    list_display = [field.name for field in PmsTenderSurveyResourceMaterial._meta.fields]


@admin.register(PmsTenderSurveyResourceEstablishment)
class PmsTenderSurveyResourceEstablishment(admin.ModelAdmin):
    list_display = [field.name for field in PmsTenderSurveyResourceEstablishment._meta.fields]


@admin.register(PmsTenderSurveyDocument)
class PmsTenderSurveyDocument(admin.ModelAdmin):
    list_display = [field.name for field in PmsTenderSurveyDocument._meta.fields]

@admin.register(PmsTenderSurveyResourceHydrological)
class PmsTenderSurveyResourceHydrological(admin.ModelAdmin):
    list_display = [field.name for field in PmsTenderSurveyResourceHydrological._meta.fields]


@admin.register(PmsTenderSurveyResourceContractorsOVendorsContractor)
class PmsTenderSurveyResourceContractorsOVendorsContractor(admin.ModelAdmin):
    list_display = [field.name for field in PmsTenderSurveyResourceContractorsOVendorsContractor._meta.fields]



@admin.register(PmsTenderSurveyResourceContractorsOVendorsVendorModelMaster)
class PmsTenderSurveyResourceContractorsOVendorsVendorModelMaster(admin.ModelAdmin):
    list_display = [field.name for field in PmsTenderSurveyResourceContractorsOVendorsVendorModelMaster._meta.fields]

@admin.register(PmsTenderSurveyResourceContractorsOVendorsVendor)
class PmsTenderSurveyResourceContractorsOVendorsVendor(admin.ModelAdmin):
    list_display = [field.name for field in PmsTenderSurveyResourceContractorsOVendorsVendor._meta.fields]


@admin.register(PmsTenderSurveyResourceContactDesignation)
class PmsTenderSurveyResourceContactDesignation(admin.ModelAdmin):
    list_display = [field.name for field in PmsTenderSurveyResourceContactDesignation._meta.fields]

@admin.register(PmsTenderSurveyResourceContactDetails)
class PmsTenderSurveyResourceContactDetails(admin.ModelAdmin):
    list_display = [field.name for field in PmsTenderSurveyResourceContactDetails._meta.fields]

@admin.register(PmsTenderInitialCosting)
class PmsTenderInitialCosting(admin.ModelAdmin):
    list_display = [field.name for field in PmsTenderInitialCosting._meta.fields]

@admin.register(PmsTenderInitialCostingExcelFieldLabel)
class PmsTenderInitialCostingExcelFieldLabel(admin.ModelAdmin):
    list_display = [field.name for field in PmsTenderInitialCostingExcelFieldLabel._meta.fields]

@admin.register(PmsTenderInitialCostingExcelFieldValue)
class PmsTenderInitialCostingExcelFieldValue(admin.ModelAdmin):
    list_display = [field.name for field in PmsTenderInitialCostingExcelFieldValue._meta.fields]

@admin.register(PmsTenderTabDocuments)
class PmsTenderTabDocuments(admin.ModelAdmin):
    list_display = [field.name for field in PmsTenderTabDocuments._meta.fields]

@admin.register(PmsTenderTabDocumentsPrice)
class PmsTenderTabDocumentsPrice(admin.ModelAdmin):
    list_display = [field.name for field in PmsTenderTabDocumentsPrice._meta.fields]


@admin.register(PmsSiteTypeProjectSiteManagement)
class PmsSiteTypeProjectSiteManagement(admin.ModelAdmin):
    list_display = [field.name for field in PmsSiteTypeProjectSiteManagement._meta.fields]


@admin.register(PmsSiteProjectSiteManagement)
class PmsSiteProjectSiteManagement(admin.ModelAdmin):
    list_display = [field.name for field in PmsSiteProjectSiteManagement._meta.fields]

@admin.register(PmsProjects)
class PmsProjects(admin.ModelAdmin):
    list_display = [field.name for field in PmsProjects._meta.fields]
    search_fields = ('name', 'project_g_id', 'start_date','end_date')

@admin.register(PmsProjectUserMapping)
class PmsProjectUserMapping(admin.ModelAdmin):
    list_display = [field.name for field in PmsProjectUserMapping._meta.fields]

@admin.register(PmsAttendance)
class PmsAttendance(admin.ModelAdmin):
    list_display = [field.name for field in PmsAttendance._meta.fields]

@admin.register(PmsAttandanceLog)
class PmsAttandanceLog(admin.ModelAdmin):
    list_display = [field.name for field in PmsAttandanceLog._meta.fields]

@admin.register(PmsMachineriesWorkingCategory)
class PmsMachineriesWorkingCategory(admin.ModelAdmin):
    list_display = [field.name for field in PmsMachineriesWorkingCategory._meta.fields]


@admin.register(PmsMachineries)
class PmsMachineries(admin.ModelAdmin):
    list_display = [field.name for field in PmsMachineries._meta.fields]

@admin.register(PmsExternalUsersType)
class PmsExternalUsersType(admin.ModelAdmin):
    list_display = [field.name for field in PmsExternalUsersType._meta.fields]

@admin.register(PmsExternalUsers)
class PmsExternalUsers(admin.ModelAdmin):
    list_display = [field.name for field in PmsExternalUsers._meta.fields]

@admin.register(PmsExternalUsersDocument)
class PmsExternalUsersDocument(admin.ModelAdmin):
    list_display = [field.name for field in PmsExternalUsersDocument._meta.fields]


@admin.register(PmsMachineriesDetailsDocument)
class PmsMachineriesDetailsDocument(admin.ModelAdmin):
    list_display = [field.name for field in PmsMachineriesDetailsDocument._meta.fields]

@admin.register(PmsMachinaryRentedTypeMaster)
class PmsMachinaryRentedTypeMaster(admin.ModelAdmin):
    list_display = [field.name for field in PmsMachinaryRentedTypeMaster._meta.fields]
@admin.register(PmsMachinaryRentedDetails)
class PmsMachinaryRentedDetails(admin.ModelAdmin):
    list_display = [field.name for field in PmsMachinaryRentedDetails._meta.fields]

@admin.register(PmsMachinaryOwnerDetails)
class PmsMachinaryOwnerDetails(admin.ModelAdmin):
    list_display = [field.name for field in PmsMachinaryOwnerDetails._meta.fields]
@admin.register(PmsMachinaryOwnerEmiDetails)
class PmsMachinaryOwnerEmiDetails(admin.ModelAdmin):
    list_display = [field.name for field in PmsMachinaryOwnerEmiDetails._meta.fields]

@admin.register(PmsMachinaryContractDetails)
class PmsMachinaryContractDetails(admin.ModelAdmin):
    list_display = [field.name for field in PmsMachinaryContractDetails._meta.fields]

@admin.register(PmsProjectsMachinaryMapping)
class PmsProjectsMachinaryMapping(admin.ModelAdmin):
    list_display = [field.name for field in PmsProjectsMachinaryMapping._meta.fields]

@admin.register(PmsProjectsMachinaryReport)
class PmsProjectsMachinaryReport(admin.ModelAdmin):
    list_display = [field.name for field in PmsProjectsMachinaryReport._meta.fields]