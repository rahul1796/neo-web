from Database import Database
class Batch:
    def batch_list(batch_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw,user_id,user_role_id):
        return Database.batch_list(batch_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw,user_id,user_role_id)
    def batch_list_updated(batch_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw,user_id,user_role_id, status, customer, project, sub_project, region, center,center_type,course_ids,batch_codes ,BU, Planned_actual, StartFromDate, StartToDate, EndFromDate, EndToDate):
        return Database.batch_list_updated(batch_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw,user_id,user_role_id, status, customer, project, sub_project, region, center, center_type,course_ids,batch_codes, BU, Planned_actual, StartFromDate, StartToDate, EndFromDate, EndToDate)
    def batch_list_assessment(batch_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw,user_id,user_role_id, status, customer, project, sub_project, region, center,center_type,course_ids,assessment_stage_id, BU, Planned_actual, StartFromDate, StartToDate, EndFromDate, EndToDate):
        return Database.batch_list_assessment(batch_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw,user_id,user_role_id, status, customer, project, sub_project, region, center, center_type,course_ids,assessment_stage_id, BU, Planned_actual, StartFromDate, StartToDate, EndFromDate, EndToDate)
    def batch_list_certification(batch_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw,user_id,user_role_id, status, customer, project, sub_project, region, center,center_type,course_ids,assessment_stage_id,certification_stage_id, BU, Planned_actual, StartFromDate, StartToDate, EndFromDate, EndToDate):
        return Database.batch_list_certification(batch_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw,user_id,user_role_id, status, customer, project, sub_project, region, center, center_type,course_ids,assessment_stage_id,certification_stage_id, BU, Planned_actual, StartFromDate, StartToDate, EndFromDate, EndToDate)
    
    def add_batch(BatchName, Product, Center, Course, SubProject, Cofunding, Trainer, isactive, PlannedStartDate, PlannedEndDate, ActualStartDate, ActualEndDate, StartTime, EndTime, BatchId, user_id, room_ids,planned_batch_id,OJTStartDate, OJTEndDate):
        popupMessage = {"PopupMessage": Database.add_batch_details(BatchName, Product, Center, Course, SubProject, Cofunding, Trainer, isactive, PlannedStartDate, PlannedEndDate, ActualStartDate, ActualEndDate, StartTime, EndTime, BatchId, user_id, room_ids,planned_batch_id,OJTStartDate, OJTEndDate)}
        return popupMessage
    def get_batch(batch_id):
        indi_batch={"BatchDetail":Database.get_batch_details(batch_id)}
        #print(indi_batch)
        return indi_batch
    def AllCourse():
        course_f={"Courses":Database.GetCourse()}
        return course_f
    def AllCenterOnCourse(course_id):
        centers_f={"Centers":Database.GetCenterBasedOnCourse(course_id)}
        return centers_f
    def AllTrainersOnCenter(center_id):
        trainers_f={"Trainers":Database.GetTrainersBasedOnCenter(center_id)}
        return trainers_f
    def AllTrainersOnSubProject(SubProject_Id):
        trainers_f={"Trainers":Database.GetTrainersBasedOnSubProject(SubProject_Id)}
        return trainers_f
    def AllCenterManagerOnCenter(center_id):
        centermanager_f={"CenterManager":Database.GetCenterManagerBasedOnCenter(center_id)}
        return centermanager_f
    def AllSubCenterOnCenter(center_id):
        subcenter_f={"SubCenter":Database.GetSubCenterBasedOnCenter(center_id)}
        return subcenter_f
    def candidate_based_on_course(candidate_id,course_ids,batch_id,center_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        return Database.candidates_based_on_course(candidate_id,course_ids,batch_id,center_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
    def candidate_maped_in_batch(candidate_id,course_ids,batch_id,center_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        return Database.candidate_maped_in_batch(candidate_id,course_ids,batch_id,center_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
    def candidate_enrolled_in_batch(batch_id,assessment_id):
        candidate={"Candidates": Database.candidate_enrolled_in_batch(batch_id,assessment_id)}
        return candidate    
    def add_edit_candidate_batch(candidate_ids,batch_id,course_id,user_id):
        popupMessage = {"PopupMessage": Database.add_edit_map_candidate_batch(candidate_ids,batch_id,course_id,user_id)}
        return popupMessage
    def drop_edit_candidate_batch(skilling_ids,batch_id,course_id,user_id,drop_remark):
        popupMessage = {"PopupMessage": Database.drop_edit_map_candidate_batch(skilling_ids,batch_id,course_id,user_id,drop_remark)}
        return popupMessage
    def tag_sponser_candidate(skilling_ids,sponser_ids,user_id):
        print("batch")
        popupMessage = {"PopupMessage": Database.tag_sponser_candidate(skilling_ids,sponser_ids,user_id)}
        return popupMessage
    def AllTrainersOnSubProject(SubProject_Id):
        trainers_f=Database.GetTrainersBasedOnSubProject(SubProject_Id)
        return trainers_f
    def AllTrainersOnSubProjects(SubProject_Id):
        trainers_f={"Trainers":Database.AllTrainersOnSubProjects(SubProject_Id)}
        return trainers_f