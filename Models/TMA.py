from Database import TMADatabase
from flask_restful import Resource
class TMA:
    def GetBatchCandidateList_db(batch_id,session_id):
        return TMADatabase.GetBatchCandidateList_db(batch_id,session_id)

    def GetSessionPlanModuleDetailsForCourse(course_id,qp_id):
        return TMADatabase.GetSessionPlanModuleDetailsForCourse(course_id,qp_id)

    def GetBatchSessionCurrentStageDetails(batch_id,session_id,user_id):
        return TMADatabase.GetBatchSessionCurrentStageDetails(batch_id,session_id,user_id)

    def GetBatchListForTMA(BatchStatusId,UserId,CenterId,role_id,app_version):
        return TMADatabase.GetBatchListForTMA(BatchStatusId,UserId,CenterId,role_id,app_version)
    
    def GetBatchSessionListForTMA(BatchId,UserId,SessionPlanId,ModuleId,StatusId,SessionName,app_version):
        return TMADatabase.GetBatchSessionListForTMA(BatchId,UserId,SessionPlanId,ModuleId,StatusId,SessionName,app_version)
    