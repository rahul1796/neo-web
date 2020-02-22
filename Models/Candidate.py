from Database import Database
class Candidate:
    def candidate_list(candidate_id,client_id,project_id,center_id,course_ids,section_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw, user_id, user_role_id):
        candidate_l = Database.candidate_list(candidate_id,client_id,project_id,center_id,course_ids,section_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw, user_id, user_role_id)
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
        print(centers)
        return centers
    def get_section_for_cand():
        section = {"Sections":Database.get_section_for_cand()}
        return section
    def get_project_basedon_client_multiple(client_id):
        projects ={"Projects": Database.get_project_basedon_client_multiple(client_id)}
        return projects