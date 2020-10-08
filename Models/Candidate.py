from Database import Database
class Candidate:
    def candidate_list(candidate_id,customer,project,sub_project,batch,region,center,center_type,status,user_id,user_role_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw, Contracts, candidate_stage, from_date, to_date):
        candidate_l = Database.candidate_list(candidate_id,customer,project,sub_project,batch,region,center,center_type,status,user_id,user_role_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw, Contracts, candidate_stage, from_date, to_date)
        return candidate_l
    def mobilized_list(candidate_id,region_ids, state_ids, MinAge, MaxAge, user_id, user_role_id, start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw,created_by,FromDate, ToDate):
        candidate_l = Database.mobilized_list(candidate_id,region_ids, state_ids, MinAge, MaxAge, user_id, user_role_id, start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw,created_by,FromDate, ToDate)
        return candidate_l
    def registered_list(candidate_id,region_ids, state_ids, Pincode, created_by, FromDate, ToDate, user_id, user_role_id, start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        candidate_l = Database.registered_list(candidate_id,region_ids, state_ids, Pincode, created_by, FromDate, ToDate, user_id, user_role_id, start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
        return candidate_l
    def enrolled_list(candidate_id,region_ids, state_ids, Pincode, created_by, FromDate, ToDate, user_id, user_role_id, start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        candidate_l = Database.enrolled_list(candidate_id,region_ids, state_ids, Pincode, created_by, FromDate, ToDate, user_id, user_role_id, start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
        return candidate_l
    def get_project_basedon_client(client_id):
        projects ={"Projects": Database.get_project_basedon_client(client_id)}
        return projects
    def get_cand_course_basedon_proj(project_id):
        courses = {"Courses": Database.get_cand_course_basedon_proj(project_id)}
        return courses
    def get_cand_course_basedon_proj_multiple(project_id):
        courses = {"Courses": Database.get_cand_course_basedon_proj_multiple(project_id)}
        return courses
    
    def get_cand_center_basedon_course(course_id):
        centers = {"Centers": Database.get_cand_center_basedon_course(course_id)}
        return centers
    def get_cand_center_basedon_course_multiple(user_id,user_role_id,course_id, RegionId):
        centers = {"Centers": Database.get_cand_center_basedon_course_multiple(user_id,user_role_id,course_id, RegionId)}
        return centers
    def get_section_for_cand():
        section = {"Sections":Database.get_section_for_cand()}
        return section
    def get_project_basedon_client_multiple(user_id,user_role_id,client_id):
        projects ={"Projects": Database.get_project_basedon_client_multiple(user_id,user_role_id,client_id)}
        return projects
    def get_allcandidate_images(user_id,user_role_id,candidate_id):
        Candidate ={"Candidate": Database.get_allcandidate_images(user_id,user_role_id,candidate_id)}
        return Candidate
    def reupload_candidate_image_web_ui(user_id,user_role_id,filename,c_id,candidate_id):
        Candidate =Database.reupload_candidate_image_web_ui(user_id,user_role_id,filename,c_id,candidate_id)
        return Candidate