from Database import Database
class Candidate:
    def candidate_list(candidate_id,customer,project,sub_project,region,center,center_type,status,user_id,user_role_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        candidate_l = Database.candidate_list(candidate_id,customer,project,sub_project,region,center,center_type,status,user_id,user_role_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
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
    def get_cand_center_basedon_course_multiple(course_id, RegionId):
        centers = {"Centers": Database.get_cand_center_basedon_course_multiple(course_id, RegionId)}
        return centers
    def get_section_for_cand():
        section = {"Sections":Database.get_section_for_cand()}
        return section
    def get_project_basedon_client_multiple(client_id):
        projects ={"Projects": Database.get_project_basedon_client_multiple(client_id)}
        return projects