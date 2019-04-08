from pms import views
from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path

from rest_framework.authtoken import views as rest_framework_views

urlpatterns = [
    #:::::::::: TENDER AND TENDER DOCUMENTS  ::::::::#
    path('tenders_add/', views.TendersAddView.as_view()),
    path('tenders_edit/<pk>/', views.TenderEditView.as_view()),
    path('tenders_delete/<pk>/', views.TenderDeleteByIdView.as_view()),
    path('tender_doc_by_tender_id/<tender_id>/', views.TenderDocsByTenderIdView.as_view()),
    path('tenders_doc_add/', views.TenderDocsAddView.as_view()),
    path('tenders_doc_edit/<pk>/', views.TenderDocsEditView.as_view()),
    path('tenders_doc_delete/<pk>/', views.TenderDocsDeleteByIdView.as_view()),

    #::::::::::::::: TENDER  BIDDER TYPE :::::::::::::::#
    path('vendors_add/', views.VendorsAddView.as_view()),
    path('tender_bidder_details_by_tender_id/<tender_id>/', views.TendorBidderTypeByTenderIdView.as_view()),
    path('tender_bidder_type_add/', views.TendorBidderTypeAddView.as_view()),
    path('tender_bidder_type_edit/<pk>/', views.TendorBidderTypeEditView.as_view()),
    path('tender_bidder_type_delete/<pk>/', views.TendorBidderTypeDeleteView.as_view()),

    #::::::::::::::: TENDER  ELIGIBILITY :::::::::::::::#
    path('tender_eligibility_fields_list/<tender_id>/<eligibility_type>/',
         views.PmsTenderEligibilityFieldsByTypeListView.as_view()),
    path('tender_eligibility_fields_add/', views.PmsTenderEligibilityAdd.as_view()),
    path('tender_eligibility_fields_edit_by_id/<pk>/', views.PmsTenderEligibilityFieldsByTypeEdit.as_view()),
    path('tender_not_eligibility_reason_add/<tender_id>/<type>/', views.PmsTenderNotEligibilityReasonAdd.as_view()),

    #::::::::::::::: TENDER SURVEY SITE PHOTOS :::::::::::::::#
    path('tender_survey_site_photos_add/', views.TenderSurveySitePhotosAddView.as_view()),
    path('tender_survey_site_photos_edit/<pk>/', views.TenderSurveySitePhotosEditView.as_view()),
    path('tender_survey_site_photos_list/<tender_id>/', views.TenderSurveySitePhotosListView.as_view()),
    path('tender_survey_site_photos_delete/<pk>/', views.TenderSurveySitePhotosDeleteView.as_view()),

    #::::::::::: TENDER SURVEY COORDINATES ::::::::::::::::::::#
    path('tender_survey_location_add/', views.TenderSurveyLocationAddView.as_view()),
    path('tender_survey_location_list/<tender_id>/', views.TenderSurveyLocationListView.as_view()),
    path('tender_survey_location_edit/<pk>/', views.TenderSurveyLocationEditView.as_view()),
    path('tender_survey_location_delete/<pk>/', views.TenderSurveyLocationDeleteView.as_view()),
    path('tender_survey_co_supplier_list/', views.TenderSurveyCOSupplierListView.as_view()),
    path('tender_survey_co_supplier_add/', views.TenderSurveyCOSupplierAddView.as_view()),
    path('tender_survey_co_supplier_edit/<pk>/', views.TenderSurveyCOSupplierEditView.as_view()),
    path('tender_survey_co_supplier_delete/<pk>/', views.TenderSurveyCOSupplierDeleteView.as_view()),
    path('tender_survey_co_supplier_document_add/', views.TenderSurveyCOSupplierDocumentAddView.as_view()),
    path('tender_survey_co_supplier_document_edit/<pk>/', views.TenderSurveyCOSupplierDocumentEditView.as_view()),
    path('tender_survey_co_supplier_document_delete/<pk>/', views.TenderSurveyCOSupplierDocumentDeleteView.as_view()),

    #::::::::::: TENDER SURVEY METERIAL ::::::::::::::::::::#
    path('tender_survey_materials_add/', views.TenderSurveyMaterialsAddView.as_view()),
    path('tender_survey_materials_edit/<pk>/', views.TenderSurveyMaterialsEditView.as_view()),
    path('tender_survey_materials_delete/<pk>/', views.TenderSurveyMaterialsDeleteView.as_view()),
    #path('tender_survey_materials_list/', views.TenderSurveyMaterialsListView.as_view()),
    path('tender_survey_materials_list/<tender_id>/', views.TenderSurveyMaterialsListByTenderView.as_view()),

    #::::::::::: TENDER SURVEY RESOURCE METERIAL SUPPLIERS ::::::::::::#
    path('tender_survey_resource_material_supplier_add/', views.TenderSurveyResourceMaterialAddView.as_view()),
    path('tender_survey_resource_material_supplier_edit/<pk>/',views.TenderSurveyResourceMaterialEditView.as_view()),
    path('tender_survey_resource_material_supplier_delete/<pk>/',views.TenderSurveyResourceMaterialDeleteView.as_view()),
    path('tender_survey_resource_material_supplier_list/',views.TenderSurveyResourceMaterialListView.as_view()),
    path('tender_survey_resource_material_supplier_document_add/', views.TenderSurveyResourceMaterialDocumentAddView.as_view()),
    path('tender_survey_resource_material_supplier_document_edit/<pk>/', views.TenderSurveyResourceMaterialDocumentEditView.as_view()),
    path('tender_survey_resource_material_supplier_document_delete/<pk>/', views.TenderSurveyResourceMaterialDocumentDeleteView.as_view()),


    #:::::::::: TENDER SURVEY RESOURCE ESTABLISHMENT :::::::::::#
    path('tender_survey_resource_establishment_add/', views.TenderSurveyResourceEstablishmentAddView.as_view()),
    path('tender_survey_resource_establishment_edit/<pk>/', views.TenderSurveyResourceEstablishmentEditView.as_view()),
    path('tender_survey_resource_establishment_delete/<pk>/', views.TenderSurveyResourceEstablishmentDeleteView.as_view()),
    path('tender_survey_resource_establishment_document_add/',views.TenderSurveyResourceEstablishmentDocumentAddView.as_view()),
    path('tender_survey_resource_establishment_document_edit/<pk>/',views.TenderSurveyResourceEstablishmentDocumentEditView.as_view()),
    path('tender_survey_resource_establishment_document_delete/<pk>/',views.TenderSurveyResourceEstablishmentDocumentDeleteView.as_view()),


    #:::: TENDER SURVEY RESOURCE HYDROLOGICAL :::::::#
    path('tender_survey_resource_hydrological_add/',views.TenderSurveyResourceHydrologicalAddView.as_view()),
    path('tender_survey_resource_hydrological_edit/<pk>/',views.TenderSurveyResourceHydrologicalEditView.as_view()),
    path('tender_survey_resource_hydrological_delete/<pk>/',views.TenderSurveyResourceHydrologicalDeleteView.as_view()),
    path('tender_survey_resource_hydrological_document_add/',views.TenderSurveyResourceHydrologicalDocumentAddView.as_view()),
    path('tender_survey_resource_hydrological_document_edit/<pk>/',views.TenderSurveyResourceHydrologicalDocumentEditView.as_view()),
    path('tender_survey_resource_hydrological_document_delete/<pk>/',views.TenderSurveyResourceHydrologicalDocumentDeleteView.as_view()),

    #:::: TENDER SURVEY RESOURCE CONTRACTORS / VENDORS :::::::#
    path('tender_survey_resource_contractors_o_vendors_contarctor_add/',views.TenderSurveyResourceContractorsOVendorsContractorAddView.as_view()),
    path('tender_survey_resource_contractors_o_vendors_contarctor_edit/<pk>/',views.TenderSurveyResourceContractorsOVendorsContractorEditView.as_view()),
    path('tender_survey_resource_contractors_o_vendors_contarctor_delete/<pk>/',views.TenderSurveyResourceContractorsOVendorsContractorDeleteView.as_view()),
    path('tender_survey_resource_contractors_o_vendors_contarctor_document_add/',views.TenderSurveyResourceContractorsOVendorsContractorDocumentAddView.as_view()),
    path('tender_survey_resource_contractors_o_vendors_contarctor_document_edit/<pk>/',views.TenderSurveyResourceContractorsOVendorsContractorDocumentEditView.as_view()),
    path('tender_survey_resource_contractors_o_vendors_contarctor_document_delete/<pk>/',views.TenderSurveyResourceContractorsOVendorsContractorDocumentDeleteView.as_view()),
    path('tender_survey_resource_contractors_o_vendors_vendor_model_master_add/',views.TenderSurveyResourceContractorsOVendorsVendorModelMasterAddView.as_view()),
    path('tender_survey_resource_contractors_o_vendors_vendor_add/',views.TenderSurveyResourceContractorsOVendorsVendorAddView.as_view()),
    path('tender_survey_resource_contractors_o_vendors_vendor_edit/<pk>/',views.TenderSurveyResourceContractorsOVendorsVendorEditView.as_view()),
    path('tender_survey_resource_contractors_o_vendors_vendor_delete/<pk>/',views.TenderSurveyResourceContractorsOVendorsVendorDeleteView.as_view()),
    path('tender_survey_resource_contractors_o_vendors_vendor_document_add/', views.TenderSurveyResourceContractorsOVendorsVendorDocumentAddView.as_view()),
    path('tender_survey_resource_contractors_o_vendors_vendor_document_edit/<pk>/', views.TenderSurveyResourceContractorsOVendorsVendorDocumentEditView.as_view()),
    path('tender_survey_resource_contractors_o_vendors_vendor_document_delete/<pk>/', views.TenderSurveyResourceContractorsOVendorsVendorDocumentDeleteView.as_view()),

    #:::: TENDER SURVEY RESOURCE CONTACT DETAILS AND DESIGNATION :::::::#
    path('tender_survey_resource_contact_designation_add/',views.TenderSurveyResourceContactDesignationAddView.as_view()),
    path('tender_survey_resource_contact_details_add/',views.TenderSurveyResourceContactDetailsAddView.as_view()),
    path('tender_survey_resource_contact_details_edit/<pk>/',views.TenderSurveyResourceContactDetailsEditView.as_view()),
    path('tender_survey_resource_contact_details_delete/<pk>/',views.TenderSurveyResourceContactDetailsDeleteView.as_view()),

    #::::::::::: TENDER INITIAL COSTING ::::::::::::::::::::#
    path('tender_initial_costing_upload_file/', views.TenderInitialCostingUploadFileView.as_view()),
    path('tender_initial_costing_add/', views.TenderInitialCostingAddView.as_view()),

    #----------Pms Site Type Project Site Management---------#
    path('project_site_management_site_type_add/', views.SiteTypeProjectSiteManagementAddView.as_view()),
    path('project_site_management_site_type_edit/<pk>/', views.SiteTypeProjectSiteManagementEditView.as_view()),
    path('project_site_management_site_type_delete/<pk>/', views.SiteTypeProjectSiteManagementDeleteView.as_view()),

    #--------- Pms Site Project Site Management---------------#
    path('project_site_management_site_add/', views.ProjectSiteManagementSiteAddView.as_view()),
    path('project_site_management_site_edit/<pk>/', views.ProjectSiteManagementSiteEditView.as_view()),
    path('project_site_management_site_delete/<pk>/', views.ProjectSiteManagementSiteDeleteView.as_view()),
    #path('project_site_management_site_wp_list/', views.ProjectSiteManagementSiteListWPView.as_view()),

    #::::::::::::::: PMS PROJECTS ::::::::::::::::::::::::::::#
    path('projects_add/', views.ProjectsAddView.as_view()),
    path('projects_list/', views.ProjectsListView.as_view()),
    path('projects_edit/<pk>/', views.ProjectsEditView.as_view()),
    path('projects_delete/<pk>/', views.ProjectsDeleteView.as_view()),

    #:::::::::::::::::  ATTENDENCE ::::::::::::::::::::#
    path('attandance_logout/<pk>/', views.AttendanceLogOutView.as_view()),
    path('attandance_add/', views.AttendanceAddView.as_view()),
    path('attandance_list_by_employee/<employee_id>/', views.AttendanceListByEmployeeView.as_view()),
    path('attandance_edit/<pk>/', views.AttendanceEditView.as_view()),
    path('attandance_approval_list/', views.AttendanceApprovalList.as_view()),
    path('attandance_approval_log_list/', views.AttandanceAllDetailsListView.as_view()),

    #::::::::::::::::: PmsAttandanceLog ::::::::::::::::::::#
    path('attandance_log_add/', views.AttandanceLogAddView.as_view()),
    path('attandance_log_edit/<pk>/', views.AttendanceLogEditView.as_view()),
    path('attandance_log_approval_edit/<pk>/', views.AttandanceLogApprovalEditView.as_view()),

    #:::::::::::::::::  PmsLeaves ::::::::::::::::::::#
    path('advance_leave_apply/', views.AdvanceLeaveAddView.as_view()),
    path('advance_leave_apply_edit/<pk>/', views.AdvanceLeaveEditView.as_view()),
    path('leave_list_by_employee/<employee_id>/', views.LeaveListByEmployeeView.as_view()),

    #:::::::::::::::::  MECHINARY WORKING CATEGORY ::::::::::::::::::::#
    path('machineries_working_category_add/', views.MachineriesWorkingCategoryAddView.as_view()),
    path('machineries_working_category_edit/<pk>/', views.MachineriesWorkingCategoryEditView.as_view()),
    path('machineries_working_category_delete/<pk>/', views.MachineriesWorkingCategoryDeleteView.as_view()),

    #:::::::::::::::::  MECHINARY ::::::::::::::::::::#
    path('machineries_add/', views.MachineriesAddView.as_view()),
    path('machineries_edit/<pk>/', views.MachineriesEditView.as_view()),
    path('machineries_list/', views.MachineriesListDetailsView.as_view()),
    path('machineries_wp_list/', views.MachineriesListWPDetailsView.as_view()),
    path('machineries_list_for_report/', views.MachineriesListForReportView.as_view()),
    path('machineries_list_filter_for_report/', views.MachineriesListFilterForReportView.as_view()),
    path('machineries_delete/<pk>/', views.MachineriesDeleteView.as_view()),
    path('machineries_details_document_add/', views.MachineriesDetailsDocumentAddView.as_view()),
    path('machineries_details_document_edit/<pk>/', views.MachineriesDetailsDocumentEditView.as_view()),
    path('machineries_details_document_delete/<pk>/', views.MachineriesDetailsDocumentDeleteView.as_view()),
    path('machineries_details_document_list/<equipment_id>/', views.MachineriesDetailsDocumentListView.as_view()),
    path('machinary_rented_type_master_add/', views.MachinaryRentedTypeMasterAddView.as_view()),
    path('machinary_rented_type_master_edit/<pk>/', views.MachinaryRentedTypeMasterEditView.as_view()),
    path('machinary_rented_type_master_delete/<pk>/', views.MachinaryRentedTypeMasterDeleteView.as_view()),


    #:::::::::::::::::  PMS External Users Type ::::::::::::::::::::#
    path('external_users_type_add/', views.ExternalUsersTypeAddView.as_view()),
    path('external_users_type_edit/<pk>/', views.ExternalUsersTypeEditView.as_view()),
    path('external_users_type_delete/<pk>/', views.ExternalUsersTypeDeleteView.as_view()),

    #:::::::::::::::::  PmsExternalUsers ::::::::::::::::::::#
    path('external_users_add/', views.ExternalUsersAddView.as_view()),
    path('external_users_edit/<pk>/', views.ExternalUsersEditView.as_view()),
    path('external_users_delete/<pk>/', views.ExternalUsersDeleteView.as_view()),
    path('external_users_document_add/', views.ExternalUsersDocumentAddView.as_view()),
    path('external_users_document_edit/<pk>/', views.ExternalUsersDocumentEditView.as_view()),
    path('external_users_document_delete/<pk>/', views.ExternalUsersDocumentDeleteView.as_view()),
    path('external_users_document_list/<external_user_id>/', views.ExternalUsersDocumentListView.as_view()),

    # -------------------------PmsTenderTabDocuments-------------------#

    path('tender_tab_document_add/', views.TenderTabDocumentAddView.as_view()),
    path('tender_tab_document_edit/<pk>/', views.TenderTabDocumentEditView.as_view()),
    path('tender_tab_document_delete/<pk>/', views.TenderTabDocumentDeleteView.as_view()),

    # ------------------------PmsTenderTabDocumentsPrice-------------------#
    path('tender_tab_document_price_add/', views.TenderTabDocumentPriceAddView.as_view()),
    path('tender_tab_document_price_edit/<pk>/', views.TenderTabDocumentPriceEditView.as_view()),
    path('tender_tab_document_price_delete/<pk>/', views.TenderTabDocumentPriceDeleteView.as_view()),

    #:::::::::::::::::::  Manpower :::::::::::::::::::::::::#
    path('manpower_list_wo_pagination/<module_id>/', views.ManPowerListWOView.as_view()),
    path('manpower_list/<module_id>/', views.ManPowerListView.as_view()),


    #:::::::::::::::::  MECHINARY REPORTS ::::::::::::::::::::#
    path('machineries_report_add/', views.MachineriesReportAddView.as_view()),
    path('machineries_report_edit/<pk>/', views.MachineriesReportEditView.as_view()),


]