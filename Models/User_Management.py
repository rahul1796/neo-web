from Database import Database
class UsersM:
    def user_role_list(user_role_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        return Database.user_role_list(user_role_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
    def add_user_role(user_role_name,user_id,is_active,user_role_id):
        popupMessage = {"PopupMessage": Database.add_user_role_details(user_role_name,user_id,is_active,user_role_id)}
        return popupMessage
    def get_user_role(glob_user_role_id):
        indi_user_role={"UserRoleDetail":Database.get_user_role_details(glob_user_role_id)}
        return indi_user_role
    def user_list(user_id,filter_role_id,user_region_id,user_role_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw, dept_ids, role_ids, entity_ids, region_ids, RM_Role_ids, R_mangager_ids,status_ids,project_ids,Act_status_id):
        return Database.user_list(user_id,filter_role_id,user_region_id,user_role_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw, dept_ids, role_ids, entity_ids, region_ids, RM_Role_ids, R_mangager_ids,status_ids,project_ids,Act_status_id)
    def add_user(user_role_id,first_name,last_name,email,mobile,created_id,is_active,user_id,Id,is_reporting_manager):
        popupMessage = {"PopupMessage": Database.add_user_details(user_role_id,first_name,last_name,email,mobile,created_id,is_active,user_id,Id,is_reporting_manager)}
        return popupMessage
    def tag_user_roles(login_user_id,user_id,neo_role,jobs_role,crm_role,isactive):
        popupMessage = {"PopupMessage": Database.tag_user_roles(login_user_id,user_id,neo_role,jobs_role,crm_role,isactive)}
        return popupMessage
    def AllUserRole():
        userrole_list={"UserRoles":Database.GetUserRole()}
        return userrole_list
    def get_user(glob_user_id):
        indi_user={"UserDetail":Database.get_user_details(glob_user_id)}
        return indi_user
    def get_user_role_details_for_role_update(user_id):
        indi_user={"UserDetail":Database.get_user_role_details_for_role_update(user_id)}
        return indi_user
    def trainer_list(user_id,user_region_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw,user_role_id,centers, status, Region_id, Cluster_id, Dept,entity_ids,project_ids,sector_ids,TrainerType):
        return Database.trainer_list(user_id,user_region_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw,user_role_id,centers, status, Region_id, Cluster_id, Dept,entity_ids,project_ids,sector_ids,TrainerType)
    def add_ex_treiner(first_name, last_name, email, mobile, trainer_tyoe, Partner, is_active, created_id):
        popupMessage = {"PopupMessage": Database.add_ex_triner_details(first_name, last_name, email, mobile, trainer_tyoe, Partner, is_active, created_id)}
        return popupMessage
    def GetUserTargets(user_id):
        return {"UserTarget":Database.GetUserTarget(user_id)}
    def add_edit_user_targer(created_by, From_Date, To_Date, product, target, is_active, user_id, user_target_id):
        popupMessage = {"PopupMessage": Database.add_edit_user_targer(created_by, From_Date, To_Date, product, target, is_active, user_id, user_target_id)}
        return popupMessage
    def AddeEdittUserAllocation(mapping_id,allocation,user_id):
        popupMessage = {"PopupMessage": Database.AddeEdittUserAllocation(mapping_id,allocation,user_id)}
        return popupMessage
