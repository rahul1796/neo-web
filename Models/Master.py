from Database import Database
from flask_restful import Resource

class Master:
    ##Center_type##
    def center_type_list(center_type_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        center_type_l =Database.center_type_list(center_type_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
        return center_type_l
    def add_center_type(center_type_name,user_id,is_active,center_type_id):
        popupMessage = {"PopupMessage": Database.add_center_type_details(center_type_name,user_id,is_active,center_type_id)}
        return popupMessage
    def get_center_type(glob_center_type_id):
        indi_center_type={"CenterTypeDetail":Database.get_center_type_details(glob_center_type_id)}
        return indi_center_type
    
    ##Center_Category##
    def center_category_list(center_category_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        center_category_l = Database.center_category_list(center_category_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
        return center_category_l
    def add_center_category(center_category_name,user_id,is_active,center_category_id):
        popupMessage = {"PopupMessage": Database.add_center_category_details(center_category_name,user_id,is_active,center_category_id)}
        return popupMessage
    def get_center_category(glob_center_category_id):
        indi_center_type={"CenterCategoryDetail":Database.get_center_category_details(glob_center_category_id)}
        return indi_center_type

    
    #Project
    def project_list(user_id,user_role_id,user_region_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw,entity,customer,p_group,block,practice,bu,product,status):
        project_l= Database.project_list(user_id,user_role_id,user_region_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw,entity,customer,p_group,block,practice,bu,product,status)
        return project_l
    def all_client(user_id,user_role_id):
        all_client={"Clients":Database.GetALLClient(user_id,user_role_id)}
        return all_client
    def add_project_details(ProjectName, ProjectCode, ClientName, ContractName, Practice, BU, projectgroup, ProjectType, Block, Product, ProjectManager, ActualEndDate, ActualStartDate, PlannedEndDate, PlannedStartDate, isactive, project_id, user_id,CourseIds):
        popupMessage = {"PopupMessage":  Database.add_project_details(ProjectName, ProjectCode, ClientName, ContractName, Practice, BU, projectgroup, ProjectType, Block, Product, ProjectManager, ActualEndDate, ActualStartDate, PlannedEndDate, PlannedStartDate, isactive, project_id, user_id,CourseIds)}
        return popupMessage
    def add_subproject_details(SubProjectName, SubProjectCode, Region, State, Centers, Course, PlannedStartDate, PlannedEndDate, ActualStartDate, ActualEndDate, user_id, subproject_id, project_code, isactive):
        popupMessage = {"PopupMessage":  Database.add_subproject_details(SubProjectName, SubProjectCode, Region, State, Centers, Course, PlannedStartDate, PlannedEndDate, ActualStartDate, ActualEndDate, user_id, subproject_id, project_code, isactive)}
        return popupMessage
    def get_project_details(glob_project_id):
        indi_project={"ProjectDetail":Database.get_project_details(glob_project_id)}
        #print(indi_project)
        return indi_project
    def get_subproject_details(glob_project_id):
        indi_project={"SubProjectDetail":Database.get_subproject_details(glob_project_id)}
        #print(indi_project)
        return indi_project


    ##Center##
    def center_list(center_id,user_id,user_role_id,user_region_id,center_type_ids,bu_ids,status,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw,regions,clusters,courses):
        center_l = Database.center_list(center_id,user_id,user_role_id,user_region_id,center_type_ids,bu_ids,status,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw,regions,clusters,courses)
        return center_l
    def add_center(center_name,user_id,is_active,center_id,center_type_id,country_id,satet_id,location_name,address,pincode,District):
        popupMessage = {"PopupMessage": Database.add_center_details(center_name,user_id,is_active,center_id,center_type_id,country_id,satet_id,location_name,address,pincode,District)}
        return popupMessage
    def AllCenters(glob_center_id):
        indi_center={"CenterDetail":Database.GetCenter(glob_center_id)}
        return indi_center
    def AllCenterTypes():
        center_t={"Center_Types":Database.GetCenterType()}
        return center_t
    def AllCenterCategory():
        center_categories={"Center_Categories":Database.GetCenterCategory()}
        return center_categories
    def AllCountry():
        countries_for={"Countries":Database.GetCountry()}
        return countries_for
    def AllStatesOnCountry(country_id):
        states_for_country={"States":Database.GetStatesBasedOnCountry(country_id)}
        return states_for_country
    def AllDistrictsOnState(state_id):
        districts_for_state={"Districts":Database.GetDistrictsBasedOnStates(state_id)}
        return districts_for_state
    def get_all_BU():
        BU={"BU":Database.get_all_BU()}
        return BU
    def get_all_Cluster_Based_On_Region(region_id):
        Cluster={"States":Database.get_all_Cluster_Based_On_Region(region_id)}
        return Cluster
    def client_list(user_id,user_role_id,client_id,Is_Active,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw, funding_sources,customer_groups,category_type_ids):
        client_l = Database.client_list(user_id,user_role_id,client_id,Is_Active,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw, funding_sources,customer_groups,category_type_ids)
        return client_l
    def add_client(client_name,client_code,user_id,is_active,client_id,FundingSource, CustomerGroup, IndustryType, CategoryType):
        popupMessage = {"PopupMessage": Database.add_client_details(client_name,client_code,user_id,is_active,client_id,FundingSource, CustomerGroup, IndustryType, CategoryType)}
        return popupMessage
    def get_client(glob_client_id):
        indi_client={"ClientDetail":Database.get_client_detail(glob_client_id)}
        return indi_client
    def get_contract(glob_contract_id):
        indi_client={"Contract_details":Database.get_contarct_detail(glob_contract_id)}
        return indi_client

    def region_list(region_id,user_id,user_role_id,user_region_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        region_l = Database.region_list(region_id,user_id,user_role_id,user_region_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
        return region_l
    def add_region(region_name,region_code,user_id,is_active,region_id):
        popupMessage = {"PopupMessage": Database.add_region_details(region_name,region_code,user_id,is_active,region_id)}
        return popupMessage
    def get_region(glob_region_id):
        indi_region={"RegionDetail":Database.get_region_detail(glob_region_id)}
        return indi_region

    
    def cluster_list(cluster_id,user_id,user_role_id,user_region_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        cluster_l = Database.cluster_list(cluster_id,user_id,user_role_id,user_region_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
        return cluster_l
    def add_cluster(cluster_name,cluster_code,region_id,user_id,is_active,cluster_id):
        popupMessage = {"PopupMessage": Database.add_cluster_details(cluster_name,cluster_code,region_id,user_id,is_active,cluster_id)}
        return popupMessage
    def get_cluster(glob_cluster_id):
        indi_cluster={"ClusterDetail":Database.get_cluster_detail(glob_cluster_id)}
        return indi_cluster
    def get_all_Region():
        Region={"Region":Database.get_all_Region()}
        return Region
    def sub_center_list(sub_center_id,parent_center_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        sub_center_l = Database.sub_center_list(sub_center_id,parent_center_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
        return sub_center_l
    def add_sub_center(sub_center_name,sub_center_loc,parent_center_id,user_id,is_active,sub_center_id):
        popupMessage = {"PopupMessage": Database.add_sub_center_details(sub_center_name,sub_center_loc,parent_center_id,user_id,is_active,sub_center_id)}
        return popupMessage
    def get_sub_center(glob_sub_center_id):
        indi_sub_center={"SubCenterDetail":Database.get_sub_center_detail(glob_sub_center_id)}
        return indi_sub_center

    def sector_list(sector_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        sector_l = Database.sector_list(sector_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
        return sector_l
    def contract_list(user_id,user_role_id,contract_id,customer_ids,stage_ids,from_date,to_date,entity_ids,sales_category_ids,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        contract_l = Database.contract_list(user_id,user_role_id,contract_id,customer_ids,stage_ids,from_date,to_date,entity_ids,sales_category_ids,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
        return contract_l
    def GetAllBusBasedOn_User(UserId,UserRoleId):
        return Database.GetAllBusBasedOn_User(UserId,UserRoleId)

    def GetAllContractStages():
        return Database.GetAllContractStages()
    
    def GetDashboardCount(UserId,UserRoleId,UserRegionId):
        return Database.GetDashboardCount(UserId,UserRoleId,UserRegionId)

    def GetDepartmentUsers(UserId,UserRoleId,UserRegionId):
        return Database.GetDepartmentUsers(UserId,UserRoleId,UserRegionId)
    def GetAllSalesCategory():
        response={"SalesCategory":Database.GetAllSalesCategory()}
        return response
    def GetAllCategoryTypes():
        response={"CategoryType":Database.GetAllCategoryTypes()}
        return response
    def GetSubProjectsForCenter(center_id):
        return Database.GetSubProjectsForCenter(center_id)
    def GetSubProjectsForCenter_course(user_id,user_role_id,center_id, course_id, sub_project_id):
        return Database.GetSubProjectsForCenter_course(user_id,user_role_id,center_id, course_id, sub_project_id)
    
    def GetProjectsForCourse(CourseId):
        return Database.GetProjectsForCourse(CourseId)
    def GetSubProjectsForCourse(CourseId):
        return Database.GetSubProjectsForCourse(CourseId)
    def GetCourseVariantsForCourse(CourseId):
        return Database.GetCourseVariantsForCourse(CourseId)
    def GetCentersForCourse(CourseId):
        return Database.GetCentersForCourse(CourseId)

    #def add_contract(ContractName, ContractCode, ClientName, EntityName, SalesCatergory, StartDate, EndDate, isactive, user_id, contract_id):
    #    popupMessage = {"PopupMessage": Database.add_contract_details(ContractName, ContractCode, ClientName, EntityName, SalesCatergory, StartDate, EndDate, isactive, user_id, contract_id)}
    #    return popupMessage
    
    def my_project_list(user_id,user_role_id,user_region_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        return Database.my_project_list(user_id,user_role_id,user_region_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
    def GetCoursesForCenter(center_id):
        return Database.GetCoursesForCenter(center_id)
    def GetCoursesForProject(project_id):
        return Database.GetCoursesForProject(project_id)
    def GetCentersForProject(project_id):
        return Database.GetCentersForProject(project_id)

    def add_contract(ContractName, ContractCode, ClientName, EntityName, SalesCatergory, StartDate, EndDate, SalesManager, ContractValue, isactive, user_id, contract_id):
        popupMessage = {"PopupMessage": Database.add_contract_details(ContractName, ContractCode, ClientName, EntityName, SalesCatergory, StartDate, EndDate, SalesManager, ContractValue, isactive, user_id, contract_id)}
        return popupMessage

    def GetSubProjectsForuser(user_id):
        return Database.GetSubProjectsForuser(user_id)
    def GetContractsBasedOnCustomer(user_id,user_role_id,customer_id):
        return Database.GetContractsBasedOnCustomer(user_id,user_role_id,customer_id)
    def GetBillingMilestones():
        return Database.GetBillingMilestones()
    def GetUnitTypes():
        return Database.GetUnitTypes()
    def SaveProjectBillingMilestones(json_string,project_id,user_id):
        return Database.SaveProjectBillingMilestones(json_string,project_id,user_id)
    def GetProjectMilestones(project_id):
        return Database.GetProjectMilestones(project_id)
    def GetSubProjectCourseMilestones(sub_project_id,course_id):
        return Database.GetSubProjectCourseMilestones(sub_project_id,course_id)
    def SaveSubProjectCourseMilestones(json_string,sub_project_id,user_id):
        return Database.SaveSubProjectCourseMilestones(json_string,sub_project_id,user_id)
    def GetCoursesBasedOnSubProject(sub_project_id):
        return Database.GetCoursesBasedOnSubProject(sub_project_id)
    def GetCentersbasedOnSubProject(sub_project_id):
        return Database.GetCentersbasedOnSubProject(sub_project_id)
    def SaveSubProjectCourseCenterUnitPrice(json_string,primary_key_id,user_id):
        return Database.SaveSubProjectCourseCenterUnitPrice(json_string,primary_key_id,user_id)
    def GetSubProjectCourseCenterUnitRates(sub_project_id,primary_key):
        return Database.GetSubProjectCourseCenterUnitRates(sub_project_id,primary_key)
    def GetContractProjectTargets(contact_id,user_id,user_role_id,region_id):
        return Database.GetContractProjectTargets(contact_id,user_id,user_role_id,region_id)
    
    def sub_project_list(user_id,user_role_id,user_region_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw,entity,customer,p_group,block,practice,bu,product,status,project):
        return Database.sub_project_list(user_id,user_role_id,user_region_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw,entity,customer,p_group,block,practice,bu,product,status,project)
    def SaveCandidateActivityStatus(json_string,user_id,latitude,longitude,timestamp,app_version,device_model,imei_num,android_version):
        return Database.SaveCandidateActivityStatus(json_string,user_id,latitude,longitude,timestamp,app_version,device_model,imei_num,android_version)
    def get_center_details(center_id):
        indi_project={"CenterDetail":Database.get_center_details(center_id)}
        return indi_project
    def GetPartnerTypes():
        response={"PartnerTypes":Database.GetPartnerTypes()}
        return response
    def partner_list(partner_type_ids,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        return Database.partner_list(partner_type_ids,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
    def add_partner_details(partner_name,user_id,is_active,partner_type_id,address,partner_id):
        popupMessage = {"PopupMessage": Database.add_partner_details(partner_name,user_id,is_active,partner_type_id,address,partner_id)}
        return popupMessage
    def get_partner_details(partner_id):
        return {"PartnerDetail":Database.get_partner_details(partner_id)}
    def GetPartnerUsers(partner_id):
        return {"PartnerUsers":Database.GetPartnerUsers(partner_id)}
    def add_edit_partner_user(UserName,user_id,is_active,Email,Mobile,PartnerId,PartnerUserId):
        popupMessage = {"PopupMessage": Database.add_edit_partner_user(UserName,user_id,is_active,Email,Mobile,PartnerId,PartnerUserId)}
        return popupMessage
    def GetPartners():
        return {'Partners':Database.GetPartners()}